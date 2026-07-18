"""
==========================================================
TikTrivia Pro
Contestant Service
Version: 0.2.0
==========================================================

Purpose
-------
Business logic for contestant management.

Author
------
Andy Arredondo / TikTrivia Pro
"""

from __future__ import annotations

from source.backend.session import close_session
from source.backend.session import get_session
from source.services.game_state import GAME
from source.repositories.contestant_repository import (
    adjust_contestant_score as repo_adjust_contestant_score,
    create_contestant,
    delete_contestant,
    get_active_contestants,
    get_all_contestants,
    get_contestant_by_id,
    reset_contestant_score as repo_reset_contestant_score,
    set_contestant_active as repo_set_contestant_active,
    update_contestant,
)


def add_contestant(
    username: str,
    display_name: str,
):
    """
    Add a new contestant.
    """

    session = get_session()

    try:

        return create_contestant(
            session=session,
            username=username,
            display_name=display_name,
        )

    finally:

        close_session(session)


def list_contestants():
    """
    Return every contestant.
    """

    session = get_session()

    try:

        return get_all_contestants(session)

    finally:

        close_session(session)


def list_active_contestants():
    """
    Return active contestants.
    """

    session = get_session()

    try:

        return get_active_contestants(session)

    finally:

        close_session(session)


def find_contestant(
    contestant_id: int,
):
    """
    Find contestant by ID.
    """

    session = get_session()

    try:

        return get_contestant_by_id(
            session,
            contestant_id,
        )

    finally:

        close_session(session)


def edit_contestant(
    contestant_id: int,
    username: str,
    display_name: str,
    active: bool,
):
    """
    Update contestant.
    """

    session = get_session()

    try:

        return update_contestant(
            session=session,
            contestant_id=contestant_id,
            username=username,
            display_name=display_name,
            active=active,
        )

    finally:

        close_session(session)


def remove_contestant(
    contestant_id: int,
):
    """
    Delete contestant.
    """

    session = get_session()

    try:

        return delete_contestant(
            session=session,
            contestant_id=contestant_id,
        )

    finally:

        close_session(session)


def reset_contestant_score(
    contestant_id: int,
):
    """
    Reset the score for a contestant.
    """

    session = get_session()

    try:

        return repo_reset_contestant_score(
            session=session,
            contestant_id=contestant_id,
        )

    finally:

        close_session(session)

def adjust_contestant_score(
    contestant_id: int,
    amount: int,
):
    """
    Add or subtract points from a contestant's score.
    """

    session = get_session()

    try:

        contestant = repo_adjust_contestant_score(
            session=session,
            contestant_id=contestant_id,
            amount=amount,
        )

        GAME.record_score_change(
            contestant_id=contestant_id,
            amount=amount,
        )

        return contestant

    finally:

        close_session(session)
def undo_last_score_change(
    contestant_id: int,
):
    """
    Undo the most recent score adjustment for one contestant.
    """

    amount = GAME.pop_last_score_change(contestant_id)

    if amount is None:
        return None

    session = get_session()

    try:

        return repo_adjust_contestant_score(
            session=session,
            contestant_id=contestant_id,
            amount=-amount,
        )

    except Exception:

        GAME.record_score_change(
            contestant_id=contestant_id,
            amount=amount,
        )

        raise

    finally:

        close_session(session)        
def set_contestant_active(
    contestant_id: int,
    active: bool,
):
    """
    Set a contestant's active state.
    """

    session = get_session()

    try:

        return repo_set_contestant_active(
            session=session,
            contestant_id=contestant_id,
            active=active,
        )

    finally:

        close_session(session)


if __name__ == "__main__":

    print()

    print("TikTrivia Pro Contestant Service")

    print("--------------------------------")

    contestants = list_contestants()

    print(f"Contestants: {len(contestants)}")

    print()