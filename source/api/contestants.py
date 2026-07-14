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

from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import HTTPException

from source.services.contestant_service import (
    add_contestant,
    edit_contestant,
    find_contestant,
    list_active_contestants,
    list_contestants,
    remove_contestant,
)

router = APIRouter(
    prefix="/api/contestants",
    tags=["Contestants"],
)


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


# ----------------------------------------------------------
# GET ALL
# ----------------------------------------------------------

@router.get("/")
async def get_contestants():

    contestants = list_contestants()

    return [

        {

            "id": contestant.id,

            "username": contestant.username,

            "display_name": contestant.display_name,

            "active": contestant.active,

            "score": contestant.score,

            "games_played": contestant.games_played,

            "correct_answers": contestant.correct_answers,

            "fastest_response_ms": contestant.fastest_response_ms,

        }

        for contestant in contestants

    ]


# ----------------------------------------------------------
# GET ACTIVE
# ----------------------------------------------------------

@router.get("/active")
async def get_active_contestants():

    contestants = list_active_contestants()

    return [

        {

            "id": contestant.id,

            "username": contestant.username,

            "display_name": contestant.display_name,

            "score": contestant.score,

        }

        for contestant in contestants

    ]


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

    return {

        "id": contestant.id,

        "username": contestant.username,

        "display_name": contestant.display_name,

        "active": contestant.active,

        "score": contestant.score,

        "games_played": contestant.games_played,

        "correct_answers": contestant.correct_answers,

        "fastest_response_ms": contestant.fastest_response_ms,

    }


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

    return {

        "success": True,

        "contestant": {

            "id": contestant.id,

            "username": contestant.username,

            "display_name": contestant.display_name,

        }

    }


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

    return {

        "success": True,

        "contestant": {

            "id": contestant.id,

            "username": contestant.username,

            "display_name": contestant.display_name,

            "active": contestant.active,

        }

    }


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

    return {

        "success": True

    }