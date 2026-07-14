"""
==========================================================
TikTrivia Pro
Family Feud API
Version 1.0
==========================================================
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from source.api.api_response import success
from source.api.api_response import failure

from source.services.familyfeud_game_service import (
    current_board,
    first_board,
    next_board,
    previous_board,
)

from source.services.game_state import GAME

router = APIRouter(
    prefix="/api/family-feud",
    tags=["Family Feud"],
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def board_to_dict(board):

    return {

        "id": board.id,

        "board_id": board.board_id,

        "category": board.category,

        "survey_question": board.survey_question,

        "answers":[

            {

                "id": answer.id,

                "rank": answer.rank,

                "answer": answer.answer,

                "points": answer.points,

                "revealed": answer.revealed,

            }

            for answer in board.answers

        ],

    }


# ---------------------------------------------------------
# Board Navigation
# ---------------------------------------------------------

@router.post("/first")
def api_first_board():

    board = first_board()

    if board is None:

        return failure(

            message="No boards found.",

            status_code=404,

        )

    GAME.load_board(board)

    return success(

        data=board_to_dict(GAME.board),

        message="First board loaded.",

    )
@router.post("/previous")
def api_previous_board():

    board = previous_board()

    if board is None:

        return failure(

            message="No boards found.",

            status_code=404,

        )

    GAME.load_board(board)

    return success(

        data=board_to_dict(GAME.board),

        message="Previous board loaded.",

    )

@router.post("/next")
def api_next_board():

    board = next_board()

    if board is None:

        return failure(

            message="No boards found.",

            status_code=404,

        )

    # Always synchronize the live game state
    GAME.load_board(board)

    return success(

        data=board_to_dict(GAME.board),

        message="Next board loaded.",

    )
# ---------------------------------------------------------
# Round Controls
# ---------------------------------------------------------

@router.post("/open")
def open_round():

    GAME.open_question()

    return success(

        data=GAME.status(),

        message="Round opened."

    )

@router.post("/close")
def close_round():

    GAME.close_question()

    return success(

        data=GAME.status(),

        message="Round closed."

    )

@router.post("/reset")
def reset_round():

    if GAME.board is None:

        return failure(

            "No board loaded.",

            status_code=400,

        )

    # Hide every answer again

    for answer in GAME.board.answers:

        answer.revealed = False

    # Reset live game state

    GAME.load_board(GAME.board)

    return success(

        data=board_to_dict(GAME.board),

        message="Round reset."

    )
@router.post("/reveal_remaining")
def reveal_remaining():

    if GAME.board is None:

        return failure(

            "No board loaded.",

            status_code=400,

        )

    GAME.answers_found.clear()

    for answer in GAME.board.answers:

        answer.revealed = True

        GAME.answers_found.append(answer.rank)

    GAME.answers_found.sort()

    return success(

        data=board_to_dict(GAME.board),

        message="Remaining answers revealed."

    )
# ---------------------------------------------------------
# Game Status
# ---------------------------------------------------------

@router.get("/status")
def game_status():

    return success(

        data=GAME.status(),

        message="Current game status."

    )

# ---------------------------------------------------------
# Current Board
# ---------------------------------------------------------

@router.get("/current")
def current():

    if GAME.board is None:

        return failure(

            "No board loaded.",

            status_code=404,

        )

    return success(

        data=board_to_dict(GAME.board),

        message="Current board.",

    )