"""
==========================================================
TikTrivia Pro
Production Models
Version 0.1.0
==========================================================

Purpose
-------
Stores reusable game productions.

A Production is an ordered collection of existing
Family Feud board IDs.

Productions DO NOT duplicate questions.

They simply reference them.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from source.backend.database import Base


# ==========================================================
# PRODUCTION
# ==========================================================

class Production(Base):

    __tablename__ = "productions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    production_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    modified: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Draft",
        nullable=False,
    )

    notes: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    tags: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    boards = relationship(
        "ProductionBoard",
        back_populates="production",
        cascade="all, delete-orphan",
        order_by="ProductionBoard.sequence",
    )


# ==========================================================
# PRODUCTION BOARD
# ==========================================================

class ProductionBoard(Base):

    __tablename__ = "production_boards"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    production_id: Mapped[int] = mapped_column(
        ForeignKey("productions.id"),
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    board_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    production = relationship(
        "Production",
        back_populates="boards",
    )


print("Production models loaded")