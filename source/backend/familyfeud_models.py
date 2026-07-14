"""
==========================================================
TikTrivia Pro
Family Feud Models
Version 0.3.0
==========================================================
"""

from __future__ import annotations

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from source.backend.database import Base


# ==========================================================
# FAMILY FEUD BOARD
# ==========================================================

class FamilyFeudBoard(Base):

    __tablename__ = "family_feud_boards"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    board_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        default="",
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        default="Intermediate",
        nullable=False,
    )

    energy: Mapped[str] = mapped_column(
        String(30),
        default="Medium",
        nullable=False,
    )

    play_time: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    survey_question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    host_opening: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    talking_points: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    hint1: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    hint2: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    reveal_script: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    audience_poll: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    chat_challenge: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    viewer_story_prompt: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    interesting_fact: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    little_known_fact: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    historical_note: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    bonus_trivia: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    tie_breaker: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    moderator_notes: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    production_notes: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    tags: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    source_reference: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    verification: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(20),
        default="1.0",
        nullable=False,
    )

    last_reviewed: Mapped[str] = mapped_column(
        String(50),
        default="",
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    answers = relationship(

        "FamilyFeudAnswer",

        back_populates="board",

        cascade="all, delete-orphan",

    )


# ==========================================================
# FAMILY FEUD ANSWERS
# ==========================================================

class FamilyFeudAnswer(Base):

    __tablename__ = "family_feud_answers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    board_id: Mapped[int] = mapped_column(
        ForeignKey("family_feud_boards.id"),
        nullable=False,
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    alternate_answers: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    reject_answers: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    points: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    revealed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    board = relationship(

        "FamilyFeudBoard",

        back_populates="answers",

    )

print("Family Feud models loaded")