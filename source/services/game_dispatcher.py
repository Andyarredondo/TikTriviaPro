"""
==========================================================
TikTrivia Pro
Game Dispatcher
Version 0.1.0
==========================================================

Purpose
-------
Route production items to the correct game engine loader.

This module does not start gameplay.
It only loads the requested item.
"""

from __future__ import annotations

from typing import Any

from source.services.familyfeud_game_service import current_board
from source.services.familyfeud_game_service import load_board


def _clean_engine(engine: str | None) -> str:
    """Normalize an engine identifier for dispatch."""

    return (engine or "").strip().lower().replace(" ", "_")


def _activate_family_feud(item_id: str) -> dict[str, Any]:
    """Load and activate a Family Feud board."""

    normalized_item_id = (item_id or "").strip()

    try:
        board = load_board(normalized_item_id)
    except Exception:
        board = None

    active_board = current_board()
    is_active = bool(
        board is not None
        and active_board is not None
        and active_board.board_id == normalized_item_id
    )

    if not is_active:
        return {
            "engine": "family_feud",
            "display_name": "Friendly Feud",
            "item_id": normalized_item_id,
            "loaded": False,
            "active": False,
            "message": "Board not found",
        }

    return {
        "engine": "family_feud",
        "display_name": "Friendly Feud",
        "item_id": normalized_item_id,
        "loaded": True,
        "active": True,
        "message": "Friendly Feud ready",
    }


def dispatch_item(engine: str, item_id: str) -> dict[str, Any]:
    """Load an item for the requested game engine."""

    normalized_engine = _clean_engine(engine)
    normalized_item_id = (item_id or "").strip()

    if normalized_engine == "family_feud":
        return _activate_family_feud(normalized_item_id)

    return {
        "engine": "unknown",
        "display_name": "Unknown",
        "item_id": normalized_item_id,
        "loaded": False,
        "active": False,
        "message": "Engine not implemented",
    }