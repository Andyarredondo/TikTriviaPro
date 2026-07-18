"""
==========================================================
TikTrivia Pro
Family Feud API
Version 1.0
==========================================================
"""

from __future__ import annotations

from fastapi import APIRouter
from source.api.api_response import success
from source.api.api_response import failure

from source.services.familyfeud_game_service import (
    current_board,
    create_random_deck,
    first_board,
    get_categories,
    next_board,
    next_random_board,
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


def board_to_dict_or_none(board):

    if board is None:
        return None

    return board_to_dict(board)


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


@router.post("/random-deck/new")
def api_new_random_deck():

    deck_ids = create_random_deck()

    if not deck_ids:

        return failure(

            message="No boards found.",

            status_code=404,

        )

    return success(

        data=GAME.random_deck_status(),

        message="Random deck created.",

    )


@router.post("/random-deck/next")
def api_next_random_board():

    board = next_random_board()

    if board is None:

        return failure(

            message="Random deck complete. Start a new deck to continue.",

            status_code=404,

        )

    return success(

        data=board_to_dict(GAME.board),

        message="Next random board loaded.",

    )


@router.get("/random-deck/status")
def random_deck_status():

    return success(

        data=GAME.random_deck_status(),

        message="Random deck status.",

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
# Registration Mode
# ---------------------------------------------------------

@router.post("/registration_mode/{mode}")
def set_registration_mode(mode: str):

    normalized_mode = mode.capitalize()

    if normalized_mode not in ("Auto", "Manual", "Hybrid"):

        return failure(

            message="Invalid registration mode.",

            status_code=400,

        )

    GAME.registration_mode = normalized_mode

    return success(

        data=GAME.status(),

        message="Registration mode updated.",

    )

# ---------------------------------------------------------
# Individual Answer Reveal
# ---------------------------------------------------------

@router.post("/reveal/{rank}")
def reveal_answer(rank: int):

    if GAME.board is None:

        return failure(

            "No board loaded.",

            status_code=400,

        )

    answer = next(

        (answer for answer in GAME.board.answers if answer.rank == rank),

        None,

    )

    if answer is None:

        return failure(

            message="Answer not found.",

            status_code=404,

        )

    if answer.revealed:

        return success(

            data=board_to_dict(GAME.board),

            message="Answer already revealed.",

        )

    answer.revealed = True

    if rank not in GAME.answers_found:

        GAME.answers_found.append(rank)

        GAME.answers_found.sort()

    return success(

        data=board_to_dict(GAME.board),

        message="Answer revealed.",

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


@router.get("/board-source")
def get_board_source():

    return success(

        data={
            "board_source": GAME.board_source,
            "selected_category": GAME.selected_category,
        },

        message="Current board source.",

    )


@router.post("/board-source/{source}")
def set_board_source(source: str):

    supported_sources = {
        "Entire Database",
        "Category",
        "Saved Show",
        "Playlist",
        "Favorites",
    }

    if source not in supported_sources:

        return failure(

            message="Invalid board source.",

            status_code=400,

        )

    GAME.board_source = source

    if source != "Category":
        GAME.selected_category = None

    create_random_deck()

    return success(

        data={
            "board_source": GAME.board_source,
            "selected_category": GAME.selected_category,
            "board": board_to_dict_or_none(GAME.board),
            "deck_status": GAME.random_deck_status(),
        },

        message="Board source updated.",

    )


@router.post("/board-source/category/{category}")
def set_category_source(category: str):

    if not category:

        return failure(

            message="Category is required.",

            status_code=400,

        )

    GAME.board_source = "Category"
    GAME.selected_category = category

    create_random_deck()

    return success(

        data={
            "board_source": GAME.board_source,
            "selected_category": GAME.selected_category,
            "board": board_to_dict_or_none(GAME.board),
            "deck_status": GAME.random_deck_status(),
        },

        message="Category selected.",

    )

@router.get("/categories")
def categories():

    return success(

        data={"categories": get_categories()},

        message="Categories loaded.",

    )