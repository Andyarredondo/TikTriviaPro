"""
==========================================================
TikTrivia Pro
Database Models
Version: 0.1.0
==========================================================

Purpose
-------
Defines the base database model structure for TikTrivia Pro.

All future database tables will inherit from the SQLAlchemy
Base class defined in database.py.

Author
------
Andy Arredondo / TikTrivia Pro
"""

from __future__ import annotations

from source.backend.database import Base


__all__ = [
    "Base"
]


if __name__ == "__main__":

    print()

    print("TikTrivia Pro Database Models")

    print("-----------------------------")

    print("Base model successfully imported.")

    print()