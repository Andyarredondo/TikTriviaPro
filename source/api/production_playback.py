"""TikTrivia Pro production playback API."""

from fastapi import APIRouter, HTTPException

from source.api.api_response import success
from source.services.production_engine import (
    ProductionError,
    current_item,
    end_production,
    get_idle_playback_state,
    next_item,
    previous_item,
    start_production,
)

router = APIRouter(
    prefix="/api/production-playback",
    tags=["Production Playback"],
)


@router.post("/start/{production_id}")
def api_start_production_playback(production_id: int):
    try:
        return success(start_production(production_id))
    except ProductionError as error:
        message = str(error)
        if "was not found" in message:
            raise HTTPException(status_code=404, detail=message)
        raise HTTPException(status_code=400, detail=message)


@router.get("/current")
def api_current_production_playback_item():
    try:
        return success(current_item())
    except ProductionError as error:
        if str(error) == "No active production.":
            return success(get_idle_playback_state())

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post("/next")
def api_next_production_playback_item():
    try:
        return success(next_item())
    except ProductionError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/previous")
def api_previous_production_playback_item():
    try:
        return success(previous_item())
    except ProductionError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/end")
def api_end_production_playback():
    return success(end_production())
