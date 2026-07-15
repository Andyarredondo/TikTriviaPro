"""
TikTrivia Pro
Production Playback API
Version 0.1.0
"""

from fastapi import APIRouter, HTTPException

from source.services.production_engine import ProductionError
from source.services.production_engine import current_item
from source.services.production_engine import end_production
from source.services.production_engine import next_item
from source.services.production_engine import previous_item
from source.services.production_engine import start_production

router = APIRouter(
    prefix="/api/production-playback",
    tags=["Production Playback"],
)


@router.post("/start/{production_id}")
def api_start_production_playback(production_id: int):
    try:
        return start_production(production_id)
    except ProductionError as error:
        message = str(error)
        if "was not found" in message:
            raise HTTPException(status_code=404, detail=message)
        raise HTTPException(status_code=400, detail=message)


@router.get("/current")
def api_current_production_playback_item():
    try:
        return current_item()
    except ProductionError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/next")
def api_next_production_playback_item():
    try:
        return next_item()
    except ProductionError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/previous")
def api_previous_production_playback_item():
    try:
        return previous_item()
    except ProductionError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/end")
def api_end_production_playback():
    return end_production()
