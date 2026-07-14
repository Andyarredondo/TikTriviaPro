"""
==========================================================
TikTrivia Pro
Database Models
Version: 0.3.0
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from source.backend.database import Base


# ==========================================================
# Contestants
# ==========================================================

class Contestant(Base):

    __tablename__ = "contestants"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    games_played: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    correct_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    fastest_response_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )


# ==========================================================
# Questions
# ==========================================================

class Question(Base):

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    question_id: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    subcategory: Mapped[str] = mapped_column(
        String(100),
        default="",
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        default="Intermediate",
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String(50),
        default="Standard",
        nullable=False,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    primary_answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    accepted_answers: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    rejected_answers: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    answer_validation: Mapped[str] = mapped_column(
        String(50),
        default="Exact",
        nullable=False,
    )

    points: Mapped[int] = mapped_column(
        Integer,
        default=100,
        nullable=False,
    )

    timer_seconds: Mapped[int] = mapped_column(
        Integer,
        default=15,
        nullable=False,
    )

    media_file: Mapped[str] = mapped_column(
        String(255),
        default="",
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    host_notes: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    source_reference: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    times_asked: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    times_correct: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    times_incorrect: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    modified_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )