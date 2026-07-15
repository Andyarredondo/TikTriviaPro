"""
TikTrivia Pro
Production API
Version 0.2.0
"""

from fastapi import APIRouter, HTTPException

from source.services.production_engine import (
    ProductionError,
    create_production,
    delete_production,
    get_production,
    list_productions,
    update_production,
)

router = APIRouter(
    prefix="/api/productions",
    tags=["Productions"],
)


def success(data):
    return {
        "success": True,
        "data": data,
    }


@router.get("")
def api_list_productions():
    return success(list_productions())


@router.get("/{production_id}")
def api_get_production(production_id: int):
    try:
        return success(get_production(production_id))
    except ProductionError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.post("")
def api_create_production(payload: dict):
    try:
        return success(
            create_production(
                production_name=payload["production_name"],
                items=payload.get("items"),
                board_ids=payload.get("board_ids"),
                description=payload.get("description", ""),
                status=payload.get("status", "Draft"),
                notes=payload.get("notes", ""),
                tags=payload.get("tags", ""),
            )
        )
    except ProductionError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.put("/{production_id}")
def api_update_production(production_id: int, payload: dict):
    try:
        return success(
            update_production(
                production_id,
                production_name=payload.get("production_name"),
                description=payload.get("description"),
                status=payload.get("status"),
                notes=payload.get("notes"),
                tags=payload.get("tags"),
                items=payload.get("items"),
                board_ids=payload.get("board_ids"),
            )
        )
    except ProductionError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.delete("/{production_id}")
def api_delete_production(production_id: int):
    try:
        return success(delete_production(production_id))
    except ProductionError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
