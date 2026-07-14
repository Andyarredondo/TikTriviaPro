"""
==========================================================
TikTrivia Pro
Question Repository
Version 0.3.0
==========================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from source.backend.models import Question


# ==========================================================
# CREATE
# ==========================================================

def create_question(

    session: Session,

    question: Question,

) -> Question:

    session.add(question)

    session.commit()

    session.refresh(question)

    return question


# ==========================================================
# GET ALL
# ==========================================================

def get_all_questions(

    session: Session,

):

    statement = (

        select(Question)

        .order_by(Question.question_id)

    )

    return list(

        session.scalars(statement).all()

    )


# ==========================================================
# GET ACTIVE
# ==========================================================

def get_active_questions(

    session: Session,

):

    statement = (

        select(Question)

        .where(Question.active == True)

        .order_by(Question.question_id)

    )

    return list(

        session.scalars(statement).all()

    )


# ==========================================================
# GET BY ID
# ==========================================================

def get_question(

    session: Session,

    question_id: int,

):

    return session.get(

        Question,

        question_id,

    )


# ==========================================================
# SEARCH BY CODE
# ==========================================================

def get_question_by_code(

    session: Session,

    code: str,

):

    statement = (

        select(Question)

        .where(

            Question.question_id == code

        )

    )

    return session.scalar(statement)


# ==========================================================
# CATEGORY
# ==========================================================

def get_questions_by_category(

    session: Session,

    category: str,

):

    statement = (

        select(Question)

        .where(

            Question.category == category

        )

    )

    return list(

        session.scalars(statement).all()

    )


# ==========================================================
# RANDOM
# ==========================================================

def get_random_question(

    session: Session,

):

    statement = (

        select(Question)

        .where(

            Question.active == True

        )

        .order_by(

            Question.id

        )

    )

    questions = list(

        session.scalars(statement).all()

    )

    if len(questions) == 0:

        return None

    import random

    return random.choice(

        questions

    )


# ==========================================================
# UPDATE
# ==========================================================

def update_question(

    session: Session,

    question: Question,

):

    session.commit()

    session.refresh(question)

    return question


# ==========================================================
# DELETE
# ==========================================================

def delete_question(

    session: Session,

    question: Question,

):

    session.delete(question)

    session.commit()