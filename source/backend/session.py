"""
==========================================================
TikTrivia Pro
Database Session Manager
Version: 0.2.0
==========================================================

Purpose
-------
Provides reusable SQLAlchemy database sessions.

Author
------
Andy Arredondo / TikTrivia Pro
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from source.backend.database import SessionLocal


def get_session() -> Session:
    """
    Create a new SQLAlchemy session.

    Returns
    -------
    Session
        Active SQLAlchemy session.
    """

    return SessionLocal()


def close_session(session: Session) -> None:
    """
    Safely close a database session.
    """

    session.close()


if __name__ == "__main__":

    session = get_session()

    print()

    print("TikTrivia Pro Database Session")

    print("------------------------------")

    print(session)

    close_session(session)

    print()

    print("Session closed successfully.")