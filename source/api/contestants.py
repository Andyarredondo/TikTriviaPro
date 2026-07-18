"""
==========================================================
TikTrivia Pro
Contestant API
Version: 0.2.0
==========================================================

Purpose
-------
REST API endpoints for contestant management.

Author
------
Andy Arredondo
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from source.api.api_response import success
from source.services.contestant_service import (
    add_contestant,
    adjust_contestant_score as service_adjust_contestant_score,
    edit_contestant,
    find_contestant,
    list_active_contestants,
    list_contestants,
    remove_contestant,
    reset_contestant_score as service_reset_contestant_score,
    set_contestant_active as service_set_contestant_active,
    undo_last_score_change as service_undo_last_score_change,
)

router = APIRouter(
    prefix="/api/contestants",
    tags=["Contestants"],
)


def contestant_to_dict(contestant, include_stats: bool = True):
    payload = {
        "id": contestant.id,
        "username": contestant.username,
        "display_name": contestant.display_name,
        "active": contestant.active,
        "score": contestant.score,
    }

    if include_stats:
        payload.update(
            {
                "games_played": contestant.games_played,
                "correct_answers": contestant.correct_answers,
                "fastest_response_ms": contestant.fastest_response_ms,
            }
        )

    return payload


# ----------------------------------------------------------
# Request Models
# ----------------------------------------------------------

class ContestantCreateRequest(BaseModel):

    username: str

    display_name: str


class ContestantUpdateRequest(BaseModel):

    username: str

    display_name: str

    active: bool

class ContestantScoreRequest(BaseModel):

    amount: int
# ----------------------------------------------------------
# GET ALL
# ----------------------------------------------------------

@router.get("/")
async def get_contestants():
    return success(
        [
            contestant_to_dict(contestant)
            for contestant in list_contestants()
        ]
    )


# ----------------------------------------------------------
# GET ACTIVE
# ----------------------------------------------------------

@router.get("/active")
async def get_active_contestants():
    return success(
        [
            contestant_to_dict(
                contestant,
                include_stats=False,
            )
            for contestant in list_active_contestants()
        ]
    )


# ----------------------------------------------------------
# GET ONE
# ----------------------------------------------------------

@router.get("/{contestant_id}")
async def get_contestant(
    contestant_id: int,
):

    contestant = find_contestant(
        contestant_id
    )

    if contestant is None:

        raise HTTPException(

            status_code=404,

            detail="Contestant not found."

        )

    return success(contestant_to_dict(contestant))


# ----------------------------------------------------------
# CREATE
# ----------------------------------------------------------

@router.post("/")
async def create_contestant(
    request: ContestantCreateRequest,
):

    contestant = add_contestant(

        username=request.username,

        display_name=request.display_name,

    )

    return success(
        contestant_to_dict(
            contestant,
            include_stats=False,
        )
    )


# ----------------------------------------------------------
# UPDATE
# ----------------------------------------------------------

@router.put("/{contestant_id}")
async def update_contestant(

    contestant_id: int,

    request: ContestantUpdateRequest,

):

    contestant = edit_contestant(

        contestant_id=contestant_id,

        username=request.username,

        display_name=request.display_name,

        active=request.active,

    )

    return success(
        contestant_to_dict(
            contestant,
            include_stats=False,
        )
    )

# ----------------------------------------------------------
# ADJUST SCORE
# ----------------------------------------------------------

@router.post("/{contestant_id}/adjust-score")
async def adjust_score(
    contestant_id: int,
    request: ContestantScoreRequest,
):

    contestant = find_contestant(contestant_id)

    if contestant is None:

        raise HTTPException(
            status_code=404,
            detail="Contestant not found.",
        )

    contestant = service_adjust_contestant_score(
        contestant_id=contestant_id,
        amount=request.amount,
    )

    return success(
        contestant_to_dict(
            contestant,
            include_stats=False,
        )
    )
# ----------------------------------------------------------
# UNDO LAST SCORE CHANGE
# ----------------------------------------------------------

@router.post("/{contestant_id}/undo-last-score")
async def undo_last_score(
    contestant_id: int,
):

    contestant = find_contestant(contestant_id)

    if contestant is None:

        raise HTTPException(
            status_code=404,
            detail="Contestant not found.",
        )

    contestant = service_undo_last_score_change(
        contestant_id=contestant_id,
    )

    if contestant is None:

        raise HTTPException(
            status_code=400,
            detail="No score change is available to undo.",
        )

    return success(
        contestant_to_dict(
            contestant,
            include_stats=False,
        )
    )

# RESET SCORE
# ----------------------------------------------------------

@router.post("/{contestant_id}/reset_score")
async def reset_contestant_score(
    contestant_id: int,
):

    contestant = find_contestant(
        contestant_id
    )

    if contestant is None:

        raise HTTPException(
            status_code=404,
            detail="Contestant not found.",
        )

    contestant = service_reset_contestant_score(
        contestant_id=contestant_id,
    )

    return success(
        contestant_to_dict(
            contestant,
            include_stats=False,
        )
    )


# ----------------------------------------------------------
# SET ACTIVE
# ----------------------------------------------------------

@router.post("/{contestant_id}/active")
async def set_contestant_active(
    contestant_id: int,
    active: bool,
):

    contestant = find_contestant(
        contestant_id
    )

    if contestant is None:

        raise HTTPException(
            status_code=404,
            detail="Contestant not found.",
        )

    contestant = service_set_contestant_active(
        contestant_id=contestant_id,
        active=active,
    )

    return success(
        contestant_to_dict(
            contestant,
            include_stats=False,
        )
    )


# ----------------------------------------------------------
# DELETE
# ----------------------------------------------------------

@router.delete("/{contestant_id}")
async def delete_contestant(
    contestant_id: int,
):

    contestant = find_contestant(
        contestant_id
    )

    if contestant is None:

        raise HTTPException(

            status_code=404,

            detail="Contestant not found."

        )

    remove_contestant(
        contestant_id
    )

    return success(None)