"""
==========================================================
TikTrivia Pro
Configuration Loader
Version: 0.1.0
==========================================================

Purpose
-------
Loads and validates the application's JSON configuration
file.

Author
------
Andy Arredondo / TikTrivia Pro

"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SETTINGS_FILE = (
    PROJECT_ROOT
    / "source"
    / "config"
    / "settings.json"
)


# ---------------------------------------------------------
# Configuration Loader
# ---------------------------------------------------------

def load_settings() -> dict[str, Any]:
    """
    Load the application settings.

    Returns
    -------
    dict
        Dictionary containing all configuration values.

    Raises
    ------
    FileNotFoundError
        If settings.json cannot be located.

    ValueError
        If settings.json contains invalid JSON.
    """

    if not SETTINGS_FILE.exists():

        raise FileNotFoundError(
            f"Settings file not found:\n{SETTINGS_FILE}"
        )

    try:

        with SETTINGS_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:

            settings = json.load(file)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Invalid JSON in settings.json\n{exc}"
        ) from exc

    return settings


# ---------------------------------------------------------
# Manual Test
# ---------------------------------------------------------

if __name__ == "__main__":

    configuration = load_settings()

    print()

    print("TikTrivia Pro Configuration")

    print("---------------------------")

    for section, values in configuration.items():

        print(section)

        print(values)

        print()