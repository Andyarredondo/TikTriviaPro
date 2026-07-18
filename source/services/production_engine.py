"""
==========================================================
TikTrivia Pro
Production Engine
Version 0.2.0
==========================================================

Purpose
-------
Create, validate, save, load, duplicate, reorder, and delete
reusable productions made from game items.

Current engine support
----------------------
- family_feud

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
from source.services.game_engine_registry import get_enabled_engines
from source.services.game_engine_registry import get_engines
from source.services.game_dispatcher import dispatch_item


VALID_STATUSES = {"Draft", "Ready", "Archived"}

_PLAYBACK_STATE = {
    "active_production_id": None,
    "current_index": 0,
}


class ProductionError(ValueError):
    """Raised when a production operation cannot be completed."""


_GAME_ENGINES = get_engines()


def get_game_engines() -> list[dict[str, Any]]:
    """Return every configured game engine."""

    return [dict(engine) for engine in _GAME_ENGINES]


def get_supported_engines() -> list[str]:
    """Return enabled engine IDs from the loaded configuration."""

    supported_engines: set[str] = set()

    for engine in get_enabled_engines():
        engine_id = str(engine.get("id") or "").strip().lower().replace(" ", "_")

        if engine_id:
            supported_engines.add(engine_id)

    return sorted(supported_engines)


SUPPORTED_ENGINES = set(get_supported_engines())


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


def _clean_engine(value: str | None) -> str:
    """Validate and normalize an item engine key."""

    engine = _clean_text(value).lower().replace(" ", "_")

    if not engine:
        raise ProductionError("Item engine is required.")

    if engine not in SUPPORTED_ENGINES:
        allowed = ", ".join(sorted(SUPPORTED_ENGINES))
        raise ProductionError(
            f"Unsupported engine '{engine}'. Supported engines: {allowed}."
        )

    return engine


def _legacy_board_ids_to_items(
    board_ids: Iterable[str] | None,
) -> list[dict[str, Any]]:
    """Convert legacy board_ids into engine-based items."""

    items: list[dict[str, Any]] = []

    for sequence, raw_board_id in enumerate(board_ids or [], start=1):
        board_id = _clean_text(raw_board_id)

        if not board_id:
            raise ProductionError("Board IDs cannot be blank.")

        items.append(
            {
                "sequence": sequence,
                "engine": "family_feud",
                "item_id": board_id,
            }
        )

    return items


def _normalize_items(
    items: Iterable[dict[str, Any]] | None = None,
    *,
    board_ids: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Normalize items while preserving supplied order.

    Backward compatibility:
    - If items are not supplied, legacy board_ids are converted to items.
    - Legacy item payloads containing board_id are accepted.
    """

    source_items = (
        list(items)
        if items is not None
        else _legacy_board_ids_to_items(board_ids)
    )

    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for raw_item in source_items:
        if isinstance(raw_item, str):
            candidate = {
                "engine": "family_feud",
                "item_id": raw_item,
            }
        elif isinstance(raw_item, dict):
            candidate = raw_item
        else:
            raise ProductionError("Each item must be an object.")

        engine = _clean_engine(candidate.get("engine", "family_feud"))
        item_id = _clean_text(
            candidate.get("item_id") or candidate.get("board_id")
        )

        if not item_id:
            raise ProductionError("Item IDs cannot be blank.")

        key = (engine, item_id)
        if key in seen:
            raise ProductionError(
                f"Duplicate item in production: {engine}:{item_id}"
            )

        seen.add(key)

        normalized.append(
            {
                "sequence": len(normalized) + 1,
                "engine": engine,
                "item_id": item_id,
            }
        )

    return normalized


def _normalize_board_ids(
    board_ids: Iterable[str] | None,
) -> list[str]:
    """Legacy helper retained for compatibility with board-specific helpers."""

    return [
        item["item_id"]
        for item in _normalize_items(board_ids=board_ids)
    ]


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


def _validate_family_feud(item_id: str) -> tuple[bool, str]:
    """Validate a Family Feud board ID."""

    session = get_session()

    try:
        statement = select(FamilyFeudBoard.id).where(
            FamilyFeudBoard.board_id == item_id
        )
        board = session.scalar(statement)

        if board is None:
            return (False, "Board not found")

        return (True, "OK")

    finally:
        close_session(session)


def validate_item(
    engine: str,
    item_id: str,
) -> tuple[bool, str]:
    """Validate one item by engine."""

    if engine == "family_feud":
        return _validate_family_feud(item_id)

    return (False, "Validation not yet implemented")


def validate_items(
    items: Iterable[dict[str, Any]] | None = None,
    *,
    board_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    """
    Validate item IDs against currently supported engines.

    Returns aggregate and per-item validation details.
    """

    normalized = _normalize_items(items, board_ids=board_ids)

    if not normalized:
        return {
            "valid": True,
            "requested_count": 0,
            "found_count": 0,
            "missing_ids": [],
            "items": [],
        }

    validated_items: list[dict[str, Any]] = []
    missing_ids: list[str] = []

    for item in normalized:
        is_valid, message = validate_item(
            item["engine"],
            item["item_id"],
        )

        validated_item = {
            "sequence": item["sequence"],
            "engine": item["engine"],
            "item_id": item["item_id"],
            "valid": is_valid,
            "message": message,
        }
        validated_items.append(validated_item)

        if (
            not is_valid
            and item["engine"] == "family_feud"
            and message == "Board not found"
        ):
            missing_ids.append(item["item_id"])

    found_count = sum(
        1 for item in validated_items if item["valid"]
    )

    return {
        "valid": found_count == len(validated_items),
        "requested_count": len(validated_items),
        "found_count": found_count,
        "missing_ids": missing_ids,
        "items": validated_items,
    }


def validate_board_ids(
    board_ids: Iterable[str] | None,
) -> dict[str, Any]:
    """Legacy board-id validation wrapper."""

    return validate_items(board_ids=board_ids)


def _validated_items(
    items: Iterable[dict[str, Any]] | None = None,
    *,
    board_ids: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Return normalized items or raise when any item is invalid."""

    normalized = _normalize_items(items, board_ids=board_ids)
    result = validate_items(normalized)

    if not result["valid"]:
        missing = ", ".join(result["missing_ids"])
        raise ProductionError(
            f"Unknown Family Feud board ID(s): {missing}"
        )

    return normalized


def _validated_board_ids(
    board_ids: Iterable[str] | None,
) -> list[str]:
    """Legacy board-id validator wrapper."""

    items = _validated_items(board_ids=board_ids)
    return [item["item_id"] for item in items]


def _rows_to_items(
    production: Production,
) -> list[dict[str, Any]]:
    """
    Convert persisted rows into generic items.

    Backward compatibility:
    Existing rows only store board_id, so they are loaded as
    family_feud items automatically.
    """

    ordered_boards = sorted(
        production.boards,
        key=lambda item: item.sequence,
    )

    return [
        {
            "sequence": item.sequence,
            "engine": "family_feud",
            "item_id": item.board_id,
        }
        for item in ordered_boards
    ]


def production_to_dict(
    production: Production,
) -> dict[str, Any]:
    """Convert an eager-loaded Production model into API-safe data."""

    items = _rows_to_items(production)

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
        "item_count": len(items),
        "items": items,
    }


def create_production(
    production_name: str,
    items: Iterable[dict[str, Any]] | None = None,
    *,
    description: str = "",
    status: str = "Draft",
    notes: str = "",
    tags: str = "",
    board_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Create and persist a new production."""

    name = _clean_name(production_name)
    normalized_items = _validated_items(
        items,
        board_ids=board_ids,
    )
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
                sequence=item["sequence"],
                board_id=item["item_id"],
            )
            for item in normalized_items
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
    items: Iterable[dict[str, Any]] | None = None,
    board_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    """
    Update production metadata and optionally replace its ordered items.

    Omitted fields remain unchanged.
    """

    normalized_items = None
    if items is not None or board_ids is not None:
        normalized_items = _validated_items(
            items,
            board_ids=board_ids,
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

        if normalized_items is not None:
            production.boards.clear()
            production.boards.extend(
                ProductionBoard(
                    sequence=item["sequence"],
                    board_id=item["item_id"],
                )
                for item in normalized_items
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
    """Delete one production and its ordered item references."""

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
        items=source["items"],
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
    """Legacy helper: add one Family Feud board item to a production."""

    production = get_production(production_id)
    items = list(production["items"])
    normalized_item = _validated_items(
        [{"engine": "family_feud", "item_id": board_id}]
    )[0]

    duplicate = next(
        (
            item
            for item in items
            if item["engine"] == "family_feud"
            and item["item_id"] == normalized_item["item_id"]
        ),
        None,
    )

    if duplicate is not None:
        raise ProductionError(
            f"Board {normalized_item['item_id']} is already in this production."
        )

    if position is None:
        items.append(normalized_item)
    else:
        if position < 1 or position > len(items) + 1:
            raise ProductionError(
                "Position must be between 1 and "
                f"{len(items) + 1}."
            )

        items.insert(position - 1, normalized_item)

    return update_production(
        production_id,
        items=items,
    )


def remove_board(
    production_id: int,
    *,
    sequence: int | None = None,
    board_id: str | None = None,
) -> dict[str, Any]:
    """Legacy helper: remove one Family Feud board item by sequence or ID."""

    if sequence is None and board_id is None:
        raise ProductionError(
            "Provide either sequence or board_id."
        )

    production = get_production(production_id)
    items = list(production["items"])

    if sequence is not None:
        if sequence < 1 or sequence > len(items):
            raise ProductionError(
                f"Sequence must be between 1 and {len(items)}."
            )

        del items[sequence - 1]

    else:
        normalized_board_id = _clean_text(board_id)

        target_index = next(
            (
                index
                for index, item in enumerate(items)
                if item["engine"] == "family_feud"
                and item["item_id"] == normalized_board_id
            ),
            None,
        )

        if target_index is None:
            raise ProductionError(
                f"Board {normalized_board_id} is not in this production."
            )

        del items[target_index]

    return update_production(
        production_id,
        items=items,
    )


def move_board(
    production_id: int,
    from_sequence: int,
    to_sequence: int,
) -> dict[str, Any]:
    """Legacy helper: move one item to a new 1-based sequence position."""

    production = get_production(production_id)
    items = list(production["items"])
    item_count = len(items)

    if from_sequence < 1 or from_sequence > item_count:
        raise ProductionError(
            f"from_sequence must be between 1 and {item_count}."
        )

    if to_sequence < 1 or to_sequence > item_count:
        raise ProductionError(
            f"to_sequence must be between 1 and {item_count}."
        )

    item = items.pop(from_sequence - 1)
    items.insert(to_sequence - 1, item)

    return update_production(
        production_id,
        items=items,
    )


def move_board_up(
    production_id: int,
    sequence: int,
) -> dict[str, Any]:
    """Legacy helper: move one item up by one position."""

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
    """Legacy helper: move one item down by one position."""

    production = get_production(production_id)
    item_count = production["item_count"]

    if sequence >= item_count:
        return production

    return move_board(
        production_id,
        sequence,
        sequence + 1,
    )


def _build_playback_payload(
    production: dict[str, Any],
    current_index: int,
) -> dict[str, Any]:
    """Build a normalized playback payload for API responses."""

    items = production.get("items") or []
    item_count = len(items)

    if item_count == 0:
        raise ProductionError(
            "Production has no items to play."
        )

    if current_index < 0:
        current_index = 0

    if current_index >= item_count:
        current_index = item_count - 1

    current = items[current_index]

    return {
        "production_id": production.get("id"),
        "production_name": production.get("production_name"),
        "current_index": current_index,
        "item_count": item_count,
        "remaining": max(item_count - (current_index + 1), 0),
        "current_item": {
            "sequence": current.get("sequence"),
            "engine": current.get("engine"),
            "item_id": current.get("item_id"),
        },
    }


def get_idle_playback_state() -> dict[str, Any]:
    """Return the normalized playback payload for an idle state."""

    return {
        "production_id": None,
        "production_name": None,
        "current_index": 0,
        "item_count": 0,
        "remaining": 0,
        "current_item": None,
        "dispatch": None,
    }


def _build_playback_response(
    production: dict[str, Any],
    current_index: int,
) -> dict[str, Any]:
    """Build playback state and dispatch the active item."""

    payload = _build_playback_payload(production, current_index)
    current_item = payload.get("current_item") or {}

    dispatch = dispatch_item(
        current_item.get("engine", ""),
        current_item.get("item_id", ""),
    )

    payload["dispatch"] = dispatch
    return payload


def start_production(
    production_id: int,
) -> dict[str, Any]:
    """Start playback for a production and position at the first item."""

    production = get_production(production_id)

    _PLAYBACK_STATE["active_production_id"] = production_id
    _PLAYBACK_STATE["current_index"] = 0

    return _build_playback_response(production, 0)


def current_item() -> dict[str, Any]:
    """Return the current playback item and dispatch the active game."""

    production_id = _PLAYBACK_STATE["active_production_id"]

    if production_id is None:
        raise ProductionError("No active production.")

    production = get_production(production_id)
    current_index = int(_PLAYBACK_STATE["current_index"])

    payload = _build_playback_response(
        production,
        current_index,
    )

    _PLAYBACK_STATE["current_index"] = payload["current_index"]

    return payload


def next_item() -> dict[str, Any]:
    """Advance playback by one item and return the new current item."""

    payload = current_item()

    item_count = payload["item_count"]
    current_index = payload["current_index"]

    if current_index < item_count - 1:
        _PLAYBACK_STATE["current_index"] = current_index + 1

    production_id = _PLAYBACK_STATE["active_production_id"]

    if production_id is None:
        raise ProductionError("No active production.")

    production = get_production(production_id)

    return _build_playback_response(
        production,
        int(_PLAYBACK_STATE["current_index"]),
    )


def previous_item() -> dict[str, Any]:
    """Move playback back by one item and return the new current item."""

    payload = current_item()

    current_index = payload["current_index"]

    if current_index > 0:
        _PLAYBACK_STATE["current_index"] = current_index - 1

    production_id = _PLAYBACK_STATE["active_production_id"]

    if production_id is None:
        raise ProductionError("No active production.")

    production = get_production(production_id)

    return _build_playback_response(
        production,
        int(_PLAYBACK_STATE["current_index"]),
    )


def end_production() -> dict[str, Any]:
    """End playback and clear active production state."""

    _PLAYBACK_STATE["active_production_id"] = None
    _PLAYBACK_STATE["current_index"] = 0

    return get_idle_playback_state()
