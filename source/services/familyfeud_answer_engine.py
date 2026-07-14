"""
==========================================================
TikTrivia Pro
Family Feud Answer Engine
Version 0.4.0
==========================================================
"""

from __future__ import annotations

import re

from source.backend.session import get_session, close_session
from source.repositories.familyfeud_repository import get_answers


def normalize(text: str) -> str:
    """
    Normalize text before comparison.
    """

    if text is None:
        return ""

    text = text.lower()

    text = text.replace("&", " and ")

    text = re.sub(r"[^\w\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def check_answer(board, player_answer: str):

    session = get_session()

    try:

        answers = get_answers(
            session,
            board.id,
        )

        player = normalize(player_answer)

        for answer in answers:

            accepted = [answer.answer]

            if answer.alternate_answers:

                accepted.extend(

                    str(answer.alternate_answers).split("|")

                )

            for value in accepted:

                if normalize(value) == player:

                    return {

                        "correct": True,

                        "rank": answer.rank,

                        "answer": answer.answer,

                        "points": answer.points,

                    }

        return {

            "correct": False

        }

    finally:

        close_session(session)