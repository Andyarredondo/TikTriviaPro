"""
==========================================================
TikTrivia Pro
Family Feud Chat Processor
Version 0.4.0
==========================================================
"""

from __future__ import annotations

from source.services.game_state import GAME
from source.services.familyfeud_answer_engine import check_answer
from source.services.familyfeud_reveal_engine import reveal_answer


def process_chat_message(

    username: str,

    message: str,

):

    """
    Process a chat message for the current board.

    Returns a dictionary describing what happened.
    """

    if GAME.board is None:

        return {

            "accepted": False,

            "reason": "no_board_loaded",

        }

    if not GAME.question_open:

        return {

            "accepted": False,

            "reason": "question_closed",

        }

    result = check_answer(

        GAME.board,

        message,

    )

    if not result["correct"]:

        return {

            "accepted": True,

            "correct": False,

        }

    if result["rank"] in GAME.answers_found:

        return {

            "accepted": True,

            "correct": False,

            "reason": "already_found",

        }

    reveal = reveal_answer(

        GAME.board,

        result["rank"],

    )

    if not reveal["success"]:

        return reveal

    GAME.correct_players[result["rank"]] = username

    return {

        "accepted": True,

        "correct": True,

        "username": username,

        "answer": reveal["answer"],

        "rank": reveal["rank"],

        "points": reveal["points"],

    }