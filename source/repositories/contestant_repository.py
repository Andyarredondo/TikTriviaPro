"""
==========================================================
TikTrivia Pro
Contestant Repository
Version: 0.2.0
==========================================================

Purpose
-------
Provides database operations for contestant records.

Author
------
Andy Arredondo / TikTrivia Pro
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from source.backend.models import Contestant


def normalize_username(username: str) -> str:
    """
    Normalize a TikTok username before storing or searching.

    Parameters
    ----------
    username:
        TikTok username entered by the host.

    Returns
    -------
    str
        Lowercase username without a leading @ symbol.

    Raises
    ------
    ValueError
        If the username is empty.
    """

    normalized = username.strip().lower()

    if normalized.startswith("@"):
        normalized = normalized[1:]

    if not normalized:
        raise ValueError("Username cannot be empty.")

    return normalized


def normalize_display_name(display_name: str) -> str:
    """
    Normalize a contestant display name.

    Parameters
    ----------
    display_name:
        Display name entered by the host.

    Returns
    -------
    str
        Trimmed display name.

    Raises
    ------
    ValueError
        If the display name is empty.
    """

    normalized = display_name.strip()

    if not normalized:
        raise ValueError("Display name cannot be empty.")

    return normalized


def create_contestant(
    session: Session,
    username: str,
    display_name: str,
) -> Contestant:
    """
    Create and save a contestant.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    username:
        TikTok username.
    display_name:
        Name shown inside TikTrivia Pro.

    Returns
    -------
    Contestant
        Newly created contestant record.

    Raises
    ------
    ValueError
        If validation fails or the username already exists.
    """

    normalized_username = normalize_username(username)
    normalized_display_name = normalize_display_name(display_name)

    existing = get_contestant_by_username(
        session=session,
        username=normalized_username,
    )

    if existing is not None:
        raise ValueError(
            f"Contestant @{normalized_username} already exists."
        )

    contestant = Contestant(
        username=normalized_username,
        display_name=normalized_display_name,
        active=True,
        score=0,
        games_played=0,
        correct_answers=0,
        fastest_response_ms=None,
    )

    session.add(contestant)

    try:
        session.commit()
        session.refresh(contestant)
    except IntegrityError as exc:
        session.rollback()
        raise ValueError(
            f"Contestant @{normalized_username} could not be created."
        ) from exc

    return contestant


def get_all_contestants(session: Session) -> list[Contestant]:
    """
    Return all contestants ordered by display name.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.

    Returns
    -------
    list[Contestant]
        All contestant records.
    """

    statement = select(Contestant).order_by(
        Contestant.display_name.asc()
    )

    return list(session.scalars(statement).all())


def get_active_contestants(session: Session) -> list[Contestant]:
    """
    Return active contestants ordered by display name.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.

    Returns
    -------
    list[Contestant]
        Active contestant records.
    """

    statement = (
        select(Contestant)
        .where(Contestant.active.is_(True))
        .order_by(Contestant.display_name.asc())
    )

    return list(session.scalars(statement).all())


def get_contestant_by_id(
    session: Session,
    contestant_id: int,
) -> Contestant | None:
    """
    Find a contestant by database ID.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    contestant_id:
        Contestant database ID.

    Returns
    -------
    Contestant | None
        Matching contestant or None.
    """

    return session.get(Contestant, contestant_id)


def get_contestant_by_username(
    session: Session,
    username: str,
) -> Contestant | None:
    """
    Find a contestant by TikTok username.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    username:
        TikTok username.

    Returns
    -------
    Contestant | None
        Matching contestant or None.
    """

    normalized_username = normalize_username(username)

    statement = select(Contestant).where(
        Contestant.username == normalized_username
    )

    return session.scalar(statement)


def update_contestant(
    session: Session,
    contestant_id: int,
    username: str,
    display_name: str,
    active: bool,
) -> Contestant:
    """
    Update a contestant record.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    contestant_id:
        Contestant database ID.
    username:
        Updated TikTok username.
    display_name:
        Updated display name.
    active:
        Whether the contestant is active.

    Returns
    -------
    Contestant
        Updated contestant record.

    Raises
    ------
    ValueError
        If the contestant does not exist or validation fails.
    """

    contestant = get_contestant_by_id(
        session=session,
        contestant_id=contestant_id,
    )

    if contestant is None:
        raise ValueError(
            f"Contestant ID {contestant_id} was not found."
        )

    normalized_username = normalize_username(username)
    normalized_display_name = normalize_display_name(display_name)

    existing = get_contestant_by_username(
        session=session,
        username=normalized_username,
    )

    if existing is not None and existing.id != contestant_id:
        raise ValueError(
            f"Contestant @{normalized_username} already exists."
        )

    contestant.username = normalized_username
    contestant.display_name = normalized_display_name
    contestant.active = active

    try:
        session.commit()
        session.refresh(contestant)
    except IntegrityError as exc:
        session.rollback()
        raise ValueError(
            f"Contestant @{normalized_username} could not be updated."
        ) from exc

    return contestant


def delete_contestant(
    session: Session,
    contestant_id: int,
) -> bool:
    """
    Delete a contestant.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    contestant_id:
        Contestant database ID.

    Returns
    -------
    bool
        True when deleted, False when not found.
    """

    contestant = get_contestant_by_id(
        session=session,
        contestant_id=contestant_id,
    )

    if contestant is None:
        return False

    session.delete(contestant)
    session.commit()

    return True


def set_contestant_active(
    session: Session,
    contestant_id: int,
    active: bool,
) -> Contestant:
    """
    Set a contestant's active state.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    contestant_id:
        Contestant database ID.
    active:
        Whether the contestant is active.

    Returns
    -------
    Contestant
        Updated contestant record.

    Raises
    ------
    ValueError
        If the contestant does not exist.
    """

    contestant = get_contestant_by_id(
        session=session,
        contestant_id=contestant_id,
    )

    if contestant is None:
        raise ValueError(
            f"Contestant ID {contestant_id} was not found."
        )

    contestant.active = active
    session.commit()
    session.refresh(contestant)

    return contestant


def reset_contestant_score(
    session: Session,
    contestant_id: int,
) -> Contestant:
    """
    Reset one contestant's current score.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.
    contestant_id:
        Contestant database ID.

    Returns
    -------
    Contestant
        Updated contestant record.

    Raises
    ------
    ValueError
        If the contestant does not exist.
    """

    contestant = get_contestant_by_id(
        session=session,
        contestant_id=contestant_id,
    )

    if contestant is None:
        raise ValueError(
            f"Contestant ID {contestant_id} was not found."
        )

    contestant.score = 0
    session.commit()
    session.refresh(contestant)

    return contestant


def reset_all_scores(session: Session) -> int:
    """
    Reset the current score for every contestant.

    Parameters
    ----------
    session:
        Active SQLAlchemy session.

    Returns
    -------
    int
        Number of contestant records reset.
    """

    contestants = get_all_contestants(session)

    for contestant in contestants:
        contestant.score = 0

    session.commit()

    return len(contestants)


if __name__ == "__main__":
    from source.backend.session import close_session
    from source.backend.session import get_session

    database_session = get_session()

    try:
        contestants = get_all_contestants(database_session)

        print()
        print("TikTrivia Pro Contestant Repository")
        print("----------------------------------")
        print(f"Contestants currently stored: {len(contestants)}")
        print()

    finally:
        close_session(database_session)