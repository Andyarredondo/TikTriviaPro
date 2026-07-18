"""TikTrivia Pro game engines API."""

from fastapi import APIRouter, HTTPException

from source.api.api_response import success
from source.services.production_engine import ProductionError
from source.services.production_engine import get_game_engines

router = APIRouter(
    prefix="/api/game-engines",
    tags=["Game Engines"],
)


@router.get("")
def api_list_game_engines():
    try:
        return success(get_game_engines())
    except ProductionError as error:
        raise HTTPException(status_code=500, detail=str(error))
