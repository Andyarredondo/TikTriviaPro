"""
==========================================================
TikTrivia Pro
Family Feud Reveal Engine
Version 0.4.0
==========================================================
"""

from __future__ import annotations

from source.backend.session import get_session
from source.backend.session import close_session

from source.repositories.familyfeud_repository import (
    get_answers,
)

from source.services.game_state import GAME


def reveal_answer(

    board,

    rank: int,

):

    """
    Reveal one answer by rank.

    Returns
    -------
    dict
    """

    session = get_session()

    try:

        answers = get_answers(

            session,

            board.id,

        )

        for answer in answers:

            if answer.rank != rank:

                continue

            if answer.revealed:

                return {

                    "success": False,

                    "reason": "already_revealed",

                }

            answer.revealed = True

            session.commit()

            GAME.answers_found.append(

                answer.rank

            )

            return {

                "success": True,

                "rank": answer.rank,

                "answer": answer.answer,

                "points": answer.points,

            }

        return {

            "success": False,

            "reason": "not_found",

        }

    finally:

        close_session(session)


def board_progress(

    board,

):

    session = get_session()

    try:

        answers = get_answers(

            session,

            board.id,

        )

        revealed = sum(

            1

            for a in answers

            if a.revealed

        )

        return {

            "revealed": revealed,

            "remaining": len(answers) - revealed,

            "total": len(answers),

        }

    finally:

        close_session(session)


def all_answers_found(

    board,

):

    progress = board_progress(

        board,

    )

    return (

        progress["remaining"] == 0

    )