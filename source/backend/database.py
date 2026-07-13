"""
==========================================================
TikTrivia Pro
Database Foundation
Version: 0.1.0
==========================================================

Purpose
-------
Initialize the SQLite database engine and SQLAlchemy session.

Author
------
Andy Arredondo / TikTrivia Pro
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIRECTORY = (
    PROJECT_ROOT
    / "source"
    / "database"
)

DATABASE_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_FILE = (
    DATABASE_DIRECTORY
    / "tiktrivia.db"
)

DATABASE_URL = (
    f"sqlite:///{DATABASE_FILE.as_posix()}"
)


# ---------------------------------------------------------
# SQLAlchemy Engine
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    """
    Base class for all database models.
    """
    pass


# ---------------------------------------------------------
# Manual Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print()

    print("TikTrivia Pro Database")

    print("----------------------")

    print(f"Database Location : {DATABASE_FILE}")

    print(f"Database Exists   : {DATABASE_FILE.exists()}")

    print()

    print("SQLAlchemy Engine Created Successfully")

    print()