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