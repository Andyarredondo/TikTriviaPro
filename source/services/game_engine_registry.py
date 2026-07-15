"""
==========================================================
TikTrivia Pro
Game Engine Registry
Version 0.1.0
==========================================================

Purpose
-------
Provide game engine metadata from a single registry source.

This module only exposes metadata.
It does not launch or activate games.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


def _registry_path() -> Path:
    """Return the shared game engine configuration path."""

    return (
        Path(__file__).resolve().parents[1]
        / "config"
        / "game_engines.json"
    )


def _clean_text(value: Any) -> str:
    """Return trimmed text for registry fields."""

    return str(value or "").strip()


def _normalize_capabilities(entry: dict[str, Any]) -> list[str]:
    """Normalize engine capabilities to a clean string list."""

    raw_capabilities = entry.get("capabilities")

    if isinstance(raw_capabilities, list):
        capabilities = [
            _clean_text(capability)
            for capability in raw_capabilities
            if _clean_text(capability)
        ]
    else:
        capabilities = []

    if entry.get("supports_productions") is True and "productions" not in capabilities:
        capabilities.append("productions")

    return capabilities


def _normalize_engine(entry: dict[str, Any]) -> dict[str, Any]:
    """Normalize a raw engine entry into registry metadata."""

    engine_id = _clean_text(entry.get("id")).lower().replace(" ", "_")
    display_name = _clean_text(entry.get("display_name") or entry.get("name"))

    if not display_name and engine_id:
        display_name = engine_id.replace("_", " ").title()

    if engine_id == "family_feud" and display_name.lower() == "family feud":
        display_name = "Friendly Feud"

    if not display_name:
        display_name = "Unknown"

    return {
        "id": engine_id,
        "display_name": display_name,
        "description": _clean_text(
            entry.get("description") or f"{display_name} engine"
        ),
        "enabled": entry.get("enabled") is True,
        "version": _clean_text(entry.get("version") or "1.0.0"),
        "icon": _clean_text(entry.get("icon")),
        "color": _clean_text(entry.get("color")),
        "capabilities": _normalize_capabilities(entry),
    }


@lru_cache(maxsize=1)
def _load_registry() -> tuple[dict[str, Any], ...]:
    """Load and normalize the engine registry from JSON."""

    config_path = _registry_path()

    if not config_path.exists():
        raise FileNotFoundError(
            f"Game engine configuration file is missing: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    engines = payload.get("engines")

    if not isinstance(engines, list):
        raise ValueError(
            "Game engine configuration must define an 'engines' list."
        )

    normalized: list[dict[str, Any]] = []

    for entry in engines:
        if not isinstance(entry, dict):
            raise ValueError("Each engine entry must be an object.")

        normalized.append(_normalize_engine(entry))

    return tuple(normalized)


def get_engines() -> list[dict[str, Any]]:
    """Return every configured engine."""

    return [dict(engine) for engine in _load_registry()]


def get_engine(engine_id: str) -> dict[str, Any] | None:
    """Return one registry entry by engine ID."""

    normalized_id = _clean_text(engine_id).lower().replace(" ", "_")

    if not normalized_id:
        return None

    for engine in _load_registry():
        if engine.get("id") == normalized_id:
            return dict(engine)

    return None


def get_enabled_engines() -> list[dict[str, Any]]:
    """Return enabled engine registry entries."""

    return [
        dict(engine)
        for engine in _load_registry()
        if engine.get("enabled") is True
    ]


def get_engine_display_name(engine_id: str) -> str:
    """Return a human-friendly display name for an engine."""

    engine = get_engine(engine_id)

    if engine is not None:
        return str(engine.get("display_name") or "Unknown")

    fallback = _clean_text(engine_id).replace("_", " ").replace("-", " ").strip()

    if not fallback:
        return "Unknown"

    return fallback.title()