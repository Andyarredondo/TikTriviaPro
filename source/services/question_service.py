"""
==========================================================
TikTrivia Pro
Question Service
Version 0.3.0
==========================================================
"""

from __future__ import annotations

from source.backend.models import Question
from source.backend.session import get_session, close_session

from source.repositories.question_repository import (
    create_question,
    get_all_questions,
    get_active_questions,
    get_question,
    get_question_by_code,
    get_questions_by_category,
    get_random_question,
    update_question,
    delete_question,
)


# ==========================================================
# CREATE
# ==========================================================

def add_question(

    question_id: str,

    category: str,

    subcategory: str,

    difficulty: str,

    question_type: str,

    question_text: str,

    primary_answer: str,

    accepted_answers: str = "",

    rejected_answers: str = "",

    answer_validation: str = "Exact",

    points: int = 100,

    timer_seconds: int = 15,

    media_file: str = "",

    explanation: str = "",

    host_notes: str = "",

    source_reference: str = "",

):

    session = get_session()

    try:

        existing = get_question_by_code(

            session,

            question_id,

        )

        if existing is not None:

            raise ValueError(

                f"Question {question_id} already exists."

            )

        question = Question(

            question_id=question_id,

            category=category,

            subcategory=subcategory,

            difficulty=difficulty,

            question_type=question_type,

            question_text=question_text,

            primary_answer=primary_answer,

            accepted_answers=accepted_answers,

            rejected_answers=rejected_answers,

            answer_validation=answer_validation,

            points=points,

            timer_seconds=timer_seconds,

            media_file=media_file,

            explanation=explanation,

            host_notes=host_notes,

            source_reference=source_reference,

        )

        return create_question(

            session,

            question,

        )

    finally:

        close_session(session)


# ==========================================================
# READ
# ==========================================================

def list_questions():

    session = get_session()

    try:

        return get_all_questions(session)

    finally:

        close_session(session)


def list_active_questions():

    session = get_session()

    try:

        return get_active_questions(session)

    finally:

        close_session(session)


def find_question(

    database_id: int,

):

    session = get_session()

    try:

        return get_question(

            session,

            database_id,

        )

    finally:

        close_session(session)


def find_question_code(

    question_code: str,

):

    session = get_session()

    try:

        return get_question_by_code(

            session,

            question_code,

        )

    finally:

        close_session(session)


def list_category(

    category: str,

):

    session = get_session()

    try:

        return get_questions_by_category(

            session,

            category,

        )

    finally:

        close_session(session)


def random_question():

    session = get_session()

    try:

        return get_random_question(

            session,

        )

    finally:

        close_session(session)


# ==========================================================
# UPDATE
# ==========================================================

def save_question(

    question: Question,

):

    session = get_session()

    try:

        return update_question(

            session,

            question,

        )

    finally:

        close_session(session)


# ==========================================================
# DELETE
# ==========================================================

def remove_question(

    question: Question,

):

    session = get_session()

    try:

        delete_question(

            session,

            question,

        )

    finally:

        close_session(session)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print()

    print("TikTrivia Pro")

    print("Question Service")

    print("----------------")

    questions = list_questions()

    print()

    print(

        f"Questions Loaded: {len(questions)}"

    )

    print()