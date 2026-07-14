"""
==========================================================
TikTrivia Pro
Question API
Version 0.3.0
==========================================================
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from source.services.question_service import (
    add_question,
    list_questions,
    list_active_questions,
    find_question,
    random_question,
)

router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"],
)


# ==========================================================
# Request Models
# ==========================================================

class QuestionCreateRequest(BaseModel):

    question_id: str

    category: str

    subcategory: str

    difficulty: str

    question_type: str

    question_text: str

    primary_answer: str

    accepted_answers: str = ""

    rejected_answers: str = ""

    answer_validation: str = "Exact"

    points: int = 100

    timer_seconds: int = 15

    media_file: str = ""

    explanation: str = ""

    host_notes: str = ""

    source_reference: str = ""


# ==========================================================
# GET ALL
# ==========================================================

@router.get("/")
async def get_questions():

    questions = list_questions()

    return questions


# ==========================================================
# GET ACTIVE
# ==========================================================

@router.get("/active")
async def get_active():

    return list_active_questions()


# ==========================================================
# RANDOM
# ==========================================================

@router.get("/random")
async def get_random():

    question = random_question()

    if question is None:

        raise HTTPException(

            status_code=404,

            detail="No active questions."

        )

    return question


# ==========================================================
# GET ONE
# ==========================================================

@router.get("/{database_id}")
async def get_question(

    database_id: int,

):

    question = find_question(

        database_id,

    )

    if question is None:

        raise HTTPException(

            status_code=404,

            detail="Question not found."

        )

    return question


# ==========================================================
# CREATE
# ==========================================================

@router.post("/")
async def create_question(

    request: QuestionCreateRequest,

):

    question = add_question(

        question_id=request.question_id,

        category=request.category,

        subcategory=request.subcategory,

        difficulty=request.difficulty,

        question_type=request.question_type,

        question_text=request.question_text,

        primary_answer=request.primary_answer,

        accepted_answers=request.accepted_answers,

        rejected_answers=request.rejected_answers,

        answer_validation=request.answer_validation,

        points=request.points,

        timer_seconds=request.timer_seconds,

        media_file=request.media_file,

        explanation=request.explanation,

        host_notes=request.host_notes,

        source_reference=request.source_reference,

    )

    return {

        "success": True,

        "database_id": question.id,

        "question_id": question.question_id,

    }