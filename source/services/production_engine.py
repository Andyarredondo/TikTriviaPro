"""
==========================================================
TikTrivia Pro
Production Engine
Version 0.1.0
==========================================================

Purpose
-------
Create, validate, save, load, duplicate, reorder, and delete
reusable productions made from existing Family Feud board IDs.

This module contains no FastAPI or React code.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from source.backend.familyfeud_models import FamilyFeudBoard
from source.backend.production_models import Production
from source.backend.production_models import ProductionBoard
from source.backend.session import close_session
from source.backend.session import get_session


VALID_STATUSES = {"Draft", "Ready", "Archived"}


class ProductionError(ValueError):
    """Raised when a production operation cannot be completed."""


def _clean_text(value: str | None) -> str:
    """Return trimmed text, using an empty string for None."""

    return (value or "").strip()


def _clean_name(value: str | None) -> str:
    """Validate and normalize a production name."""

    name = _clean_text(value)

    if not name:
        raise ProductionError("Production name is required.")

    if len(name) > 150:
        raise ProductionError(
            "Production name cannot exceed 150 characters."
        )

    return name


def _clean_status(value: str | None) -> str:
    """Validate and normalize a production status."""

    status = _clean_text(value) or "Draft"

    if status not in VALID_STATUSES:
        valid = ", ".join(sorted(VALID_STATUSES))
        raise ProductionError(
            f"Invalid production status. Expected one of: {valid}."
        )

    return status


def _normalize_board_ids(
    board_ids: Iterable[str] | None,
) -> list[str]:
    """
    Normalize board IDs while preserving their supplied order.

    Duplicate IDs are rejected because a manually assembled production
    should not silently repeat the same board.
    """

    normalized: list[str] = []
    seen: set[str] = set()

    for raw_board_id in board_ids or []:
        board_id = _clean_text(raw_board_id)

        if not board_id:
            raise ProductionError("Board IDs cannot be blank.")

        if board_id in seen:
            raise ProductionError(
                f"Duplicate board ID in production: {board_id}"
            )

        seen.add(board_id)
        normalized.append(board_id)

    return normalized


def _production_statement():
    """Return the standard eager-loaded Production query."""

    return select(Production).options(
        selectinload(Production.boards)
    )


def _get_production_or_raise(
    session,
    production_id: int,
) -> Production:
    """Load one production or raise a clear error."""

    statement = (
        _production_statement()
        .where(Production.id == production_id)
    )

    production = session.scalar(statement)

    if production is None:
        raise ProductionError(
            f"Production {production_id} was not found."
        )

    return production


def _ensure_unique_name(
    session,
    production_name: str,
    *,
    exclude_production_id: int | None = None,
) -> None:
    """Reject duplicate production names."""

    statement = select(Production.id).where(
        Production.production_name == production_name
    )

    if exclude_production_id is not None:
        statement = statement.where(
            Production.id != exclude_production_id
        )

    existing_id = session.scalar(statement)

    if existing_id is not None:
        raise ProductionError(
            f'A production named "{production_name}" already exists.'
        )


def validate_board_ids(
    board_ids: Iterable[str] | None,
) -> dict[str, Any]:
    """
    Validate board IDs against the Family Feud board library.

    Returns a structured result that preserves the requested order.
    """

    normalized = _normalize_board_ids(board_ids)

    if not normalized:
        return {
            "valid": True,
            "requested_count": 0,
            "found_count": 0,
            "missing_ids": [],
            "boards": [],
        }

    session = get_session()

    try:
        statement = select(FamilyFeudBoard).where(
            FamilyFeudBoard.board_id.in_(normalized)
        )

        rows = list(session.scalars(statement).all())
        by_id = {board.board_id: board for board in rows}

        missing_ids = [
            board_id
            for board_id in normalized
            if board_id not in by_id
        ]

        boards = [
            {
                "board_id": board_id,
                "category": by_id[board_id].category,
                "difficulty": by_id[board_id].difficulty,
                "survey_question": by_id[board_id].survey_question,
                "active": by_id[board_id].active,
            }
            for board_id in normalized
            if board_id in by_id
        ]

        return {
            "valid": not missing_ids,
            "requested_count": len(normalized),
            "found_count": len(boards),
            "missing_ids": missing_ids,
            "boards": boards,
        }

    finally:
        close_session(session)


def _validated_board_ids(
    board_ids: Iterable[str] | None,
) -> list[str]:
    """Return normalized board IDs or raise when any ID is invalid."""

    normalized = _normalize_board_ids(board_ids)
    result = validate_board_ids(normalized)

    if not result["valid"]:
        missing = ", ".join(result["missing_ids"])
        raise ProductionError(
            f"Unknown Family Feud board ID(s): {missing}"
        )

    return normalized


def production_to_dict(
    production: Production,
) -> dict[str, Any]:
    """Convert an eager-loaded Production model into API-safe data."""

    ordered_boards = sorted(
        production.boards,
        key=lambda item: item.sequence,
    )

    return {
        "id": production.id,
        "production_name": production.production_name,
        "description": production.description,
        "created": (
            production.created.isoformat()
            if production.created
            else None
        ),
        "modified": (
            production.modified.isoformat()
            if production.modified
            else None
        ),
        "status": production.status,
        "notes": production.notes,
        "tags": production.tags,
        "board_count": len(ordered_boards),
        "board_ids": [
            item.board_id
            for item in ordered_boards
        ],
        "boards": [
            {
                "id": item.id,
                "sequence": item.sequence,
                "board_id": item.board_id,
            }
            for item in ordered_boards
        ],
    }


def create_production(
    production_name: str,
    board_ids: Iterable[str] | None = None,
    *,
    description: str = "",
    status: str = "Draft",
    notes: str = "",
    tags: str = "",
) -> dict[str, Any]:
    """Create and persist a new production."""

    name = _clean_name(production_name)
    normalized_ids = _validated_board_ids(board_ids)
    normalized_status = _clean_status(status)

    session = get_session()

    try:
        _ensure_unique_name(session, name)

        production = Production(
            production_name=name,
            description=_clean_text(description),
            status=normalized_status,
            notes=_clean_text(notes),
            tags=_clean_text(tags),
            created=datetime.utcnow(),
            modified=datetime.utcnow(),
        )

        production.boards = [
            ProductionBoard(
                sequence=index,
                board_id=board_id,
            )
            for index, board_id in enumerate(
                normalized_ids,
                start=1,
            )
        ]

        session.add(production)
        session.commit()

        production = _get_production_or_raise(
            session,
            production.id,
        )

        return production_to_dict(production)

    except Exception:
        session.rollback()
        raise

    finally:
        close_session(session)


def list_productions(
    *,
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    """Return saved productions ordered by most recently modified."""

    session = get_session()

    try:
        statement = _production_statement()

        if not include_archived:
            statement = statement.where(
                Production.status != "Archived"
            )

        statement = statement.order_by(
            Production.modified.desc(),
            Production.production_name.asc(),
        )

        productions = list(
            session.scalars(statement).unique().all()
        )

        return [
            production_to_dict(production)
            for production in productions
        ]

    finally:
        close_session(session)


def get_production(
    production_id: int,
) -> dict[str, Any]:
    """Return one saved production."""

    session = get_session()

    try:
        production = _get_production_or_raise(
            session,
            production_id,
        )

        return production_to_dict(production)

    finally:
        close_session(session)


def update_production(
    production_id: int,
    *,
    production_name: str | None = None,
    description: str | None = None,
    status: str | None = None,
    notes: str | None = None,
    tags: str | None = None,
    board_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    """
    Update production metadata and optionally replace its ordered boards.

    Omitted fields remain unchanged.
    """

    normalized_ids = (
        _validated_board_ids(board_ids)
        if board_ids is not None
        else None
    )

    session = get_session()

    try:
        production = _get_production_or_raise(
            session,
            production_id,
        )

        if production_name is not None:
            name = _clean_name(production_name)
            _ensure_unique_name(
                session,
                name,
                exclude_production_id=production.id,
            )
            production.production_name = name

        if description is not None:
            production.description = _clean_text(description)

        if status is not None:
            production.status = _clean_status(status)

        if notes is not None:
            production.notes = _clean_text(notes)

        if tags is not None:
            production.tags = _clean_text(tags)

        if normalized_ids is not None:
            production.boards.clear()
            production.boards.extend(
                ProductionBoard(
                    sequence=index,
                    board_id=board_id,
                )
                for index, board_id in enumerate(
                    normalized_ids,
                    start=1,
                )
            )

        production.modified = datetime.utcnow()

        session.commit()

        production = _get_production_or_raise(
            session,
            production.id,
        )

        return production_to_dict(production)

    except Exception:
        session.rollback()
        raise

    finally:
        close_session(session)


def delete_production(
    production_id: int,
) -> dict[str, Any]:
    """Delete one production and its ordered board references."""

    session = get_session()

    try:
        production = _get_production_or_raise(
            session,
            production_id,
        )

        deleted = production_to_dict(production)

        session.delete(production)
        session.commit()

        return deleted

    except Exception:
        session.rollback()
        raise

    finally:
        close_session(session)


def duplicate_production(
    production_id: int,
    new_name: str,
) -> dict[str, Any]:
    """Create an independent copy of an existing production."""

    source = get_production(production_id)

    return create_production(
        production_name=new_name,
        board_ids=source["board_ids"],
        description=source["description"],
        status="Draft",
        notes=source["notes"],
        tags=source["tags"],
    )


def add_board(
    production_id: int,
    board_id: str,
    *,
    position: int | None = None,
) -> dict[str, Any]:
    """Add one validated board to a production."""

    production = get_production(production_id)
    board_ids = list(production["board_ids"])
    normalized_board_id = _validated_board_ids([board_id])[0]

    if normalized_board_id in board_ids:
        raise ProductionError(
            f"Board {normalized_board_id} is already in this production."
        )

    if position is None:
        board_ids.append(normalized_board_id)
    else:
        if position < 1 or position > len(board_ids) + 1:
            raise ProductionError(
                "Position must be between 1 and "
                f"{len(board_ids) + 1}."
            )

        board_ids.insert(position - 1, normalized_board_id)

    return update_production(
        production_id,
        board_ids=board_ids,
    )


def remove_board(
    production_id: int,
    *,
    sequence: int | None = None,
    board_id: str | None = None,
) -> dict[str, Any]:
    """Remove one board by sequence number or board ID."""

    if sequence is None and board_id is None:
        raise ProductionError(
            "Provide either sequence or board_id."
        )

    production = get_production(production_id)
    board_ids = list(production["board_ids"])

    if sequence is not None:
        if sequence < 1 or sequence > len(board_ids):
            raise ProductionError(
                f"Sequence must be between 1 and {len(board_ids)}."
            )

        del board_ids[sequence - 1]

    else:
        normalized_board_id = _clean_text(board_id)

        if normalized_board_id not in board_ids:
            raise ProductionError(
                f"Board {normalized_board_id} is not in this production."
            )

        board_ids.remove(normalized_board_id)

    return update_production(
        production_id,
        board_ids=board_ids,
    )


def move_board(
    production_id: int,
    from_sequence: int,
    to_sequence: int,
) -> dict[str, Any]:
    """Move one board to a new 1-based sequence position."""

    production = get_production(production_id)
    board_ids = list(production["board_ids"])
    board_count = len(board_ids)

    if from_sequence < 1 or from_sequence > board_count:
        raise ProductionError(
            f"from_sequence must be between 1 and {board_count}."
        )

    if to_sequence < 1 or to_sequence > board_count:
        raise ProductionError(
            f"to_sequence must be between 1 and {board_count}."
        )

    item = board_ids.pop(from_sequence - 1)
    board_ids.insert(to_sequence - 1, item)

    return update_production(
        production_id,
        board_ids=board_ids,
    )


def move_board_up(
    production_id: int,
    sequence: int,
) -> dict[str, Any]:
    """Move one board up by one position."""

    if sequence <= 1:
        return get_production(production_id)

    return move_board(
        production_id,
        sequence,
        sequence - 1,
    )


def move_board_down(
    production_id: int,
    sequence: int,
) -> dict[str, Any]:
    """Move one board down by one position."""

    production = get_production(production_id)
    board_count = production["board_count"]

    if sequence >= board_count:
        return production

    return move_board(
        production_id,
        sequence,
        sequence + 1,
    )
