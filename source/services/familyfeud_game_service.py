"""
==========================================================
TikTrivia Pro
Family Feud Game Service
Version 0.4.1
==========================================================

Purpose
-------
Loads Family Feud boards together with their answers before
the database session closes.
"""

from __future__ import annotations

import random

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from source.backend.familyfeud_models import FamilyFeudBoard
from source.backend.session import close_session
from source.backend.session import get_session
from source.services.game_state import GAME


_current_board: FamilyFeudBoard | None = None


def _board_query():
    """
    Return the standard board query with answers preloaded.
    """

    return select(FamilyFeudBoard).options(
        selectinload(FamilyFeudBoard.answers)
    )


def _activate_board(
    board: FamilyFeudBoard | None,
) -> FamilyFeudBoard | None:
    """
    Store a board in memory and initialize the live game state.
    """

    global _current_board

    if board is None:
        return None

    board.answers.sort(
        key=lambda answer: answer.rank
    )

    _current_board = board

    GAME.load_board(board)

    return board


def load_board(
    board_id: str,
) -> FamilyFeudBoard | None:
    """
    Load a board by its permanent board ID.
    """

    session = get_session()

    try:
        statement = (
            _board_query()
            .where(
                FamilyFeudBoard.board_id == board_id.strip()
            )
        )

        board = session.scalar(statement)

        return _activate_board(board)

    finally:
        close_session(session)


def current_board() -> FamilyFeudBoard | None:
    """
    Return the currently loaded board.
    """

    return _current_board


def clear_board() -> None:
    """
    Remove the current board and reset live game state.
    """

    global _current_board

    _current_board = None

    GAME.reset()


def _get_all_boards() -> list[FamilyFeudBoard]:
    """
    Load every board with its answers.
    """

    session = get_session()

    try:
        statement = (
            _board_query()
            .order_by(FamilyFeudBoard.board_id)
        )

        boards = list(
            session.scalars(statement).all()
        )

        for board in boards:
            board.answers.sort(
                key=lambda answer: answer.rank
            )

        return boards

    finally:
        close_session(session)


def _get_boards_for_category(category: str) -> list[FamilyFeudBoard]:
    """
    Load boards for a single category with their answers.
    """

    session = get_session()

    try:
        statement = (
            _board_query()
            .where(FamilyFeudBoard.category == category)
            .order_by(FamilyFeudBoard.board_id)
        )

        boards = list(
            session.scalars(statement).all()
        )

        for board in boards:
            board.answers.sort(
                key=lambda answer: answer.rank
            )

        return boards

    finally:
        close_session(session)


def get_categories() -> list[str]:
    """
    Return all unique board categories, sorted alphabetically.
    """

    session = get_session()

    try:
        statement = select(FamilyFeudBoard.category).distinct()
        categories = list(session.scalars(statement).all())
        return sorted(
            category for category in categories if category
        )

    finally:
        close_session(session)


def _get_boards_for_current_source() -> list[FamilyFeudBoard]:
    """
    Return boards for the currently selected source.
    """

    if GAME.board_source == "Category":
        return _get_boards_for_category(GAME.selected_category or "")

    return _get_all_boards()


def create_random_deck() -> list[str]:
    """
    Create a new shuffled deck containing every board exactly once.
    """

    boards = _get_boards_for_current_source()

    if not boards:
        GAME.random_deck_ids = []
        GAME.random_deck_position = 0
        GAME.random_deck_last_played = []
        return []

    shuffled_board_ids = [board.board_id for board in boards]

    for index in range(len(shuffled_board_ids) - 1, 0, -1):
        swap_index = random.randrange(index + 1)
        shuffled_board_ids[index], shuffled_board_ids[swap_index] = (
            shuffled_board_ids[swap_index],
            shuffled_board_ids[index],
        )

    GAME.random_deck_ids = shuffled_board_ids
    GAME.random_deck_position = 0
    GAME.random_deck_last_played = []

    first_board_id = shuffled_board_ids[0] if shuffled_board_ids else None

    if first_board_id:
        board_lookup = {board.board_id: board for board in boards}
        first_board = board_lookup.get(first_board_id)

        if first_board is not None:
            _activate_board(first_board)

    return shuffled_board_ids


def next_random_board() -> FamilyFeudBoard | None:
    """
    Load the next board from the shuffled random deck.
    """

    boards = _get_boards_for_current_source()

    if not boards:
        return None

    if not GAME.random_deck_ids or GAME.random_deck_position >= len(GAME.random_deck_ids):
        return None

    board_id = GAME.random_deck_ids[GAME.random_deck_position]
    GAME.random_deck_position += 1

    board = next(
        (board for board in boards if board.board_id == board_id),
        None,
    )

    if board is None:
        return None

    GAME.record_random_deck_played(board.board_id)

    return _activate_board(board)


def first_board() -> FamilyFeudBoard | None:
    """
    Load the first board alphabetically.
    """

    boards = _get_all_boards()

    if not boards:
        return None

    return _activate_board(boards[0])


def next_board() -> FamilyFeudBoard | None:
    """
    Load the next board alphabetically.

    The sequence wraps to the first board after the last board.
    """

    boards = _get_all_boards()

    if not boards:
        return None

    if _current_board is None:
        return _activate_board(boards[0])

    current_index = next(
        (
            index
            for index, board in enumerate(boards)
            if board.board_id == _current_board.board_id
        ),
        None,
    )

    if current_index is None:
        return _activate_board(boards[0])

    next_index = (current_index + 1) % len(boards)

    return _activate_board(
        boards[next_index]
    )


def previous_board() -> FamilyFeudBoard | None:
    """
    Load the previous board alphabetically.

    The sequence wraps to the last board before the first board.
    """

    boards = _get_all_boards()

    if not boards:
        return None

    if _current_board is None:
        return _activate_board(boards[0])

    current_index = next(
        (
            index
            for index, board in enumerate(boards)
            if board.board_id == _current_board.board_id
        ),
        None,
    )

    if current_index is None:
        return _activate_board(boards[0])

    previous_index = (
        current_index - 1
    ) % len(boards)

    return _activate_board(
        boards[previous_index]
    )