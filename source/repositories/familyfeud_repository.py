"""
==========================================================
TikTrivia Pro
Family Feud Repository
Version 0.3.0
==========================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from source.backend.familyfeud_models import (
    FamilyFeudBoard,
    FamilyFeudAnswer,
)


# ==========================================================
# BOARD
# ==========================================================

def create_board(
    session: Session,
    board: FamilyFeudBoard,
):

    session.add(board)
    session.commit()
    session.refresh(board)

    return board


def get_board_by_code(
    session: Session,
    board_id: str,
):

    statement = (
        select(FamilyFeudBoard)
        .where(FamilyFeudBoard.board_id == board_id)
    )

    return session.scalar(statement)


def get_all_boards(
    session: Session,
):

    statement = (
        select(FamilyFeudBoard)
        .order_by(FamilyFeudBoard.board_id)
    )

    return list(session.scalars(statement).all())


# ==========================================================
# ANSWERS
# ==========================================================

def create_answer(
    session: Session,
    answer: FamilyFeudAnswer,
):

    session.add(answer)
    session.commit()
    session.refresh(answer)

    return answer


def get_answers(
    session: Session,
    board_database_id: int,
):

    statement = (
        select(FamilyFeudAnswer)
        .where(FamilyFeudAnswer.board_id == board_database_id)
        .order_by(FamilyFeudAnswer.rank)
    )

    return list(session.scalars(statement).all())