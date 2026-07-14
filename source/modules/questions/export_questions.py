"""
==========================================================
TikTrivia Pro
Question Export Engine
Version 0.3.0
==========================================================
"""

from __future__ import annotations

import pandas as pd

from source.services.question_service import list_questions


def export_excel(file_name: str):

    questions = list_questions()

    rows = []

    for question in questions:

        rows.append(

            {

                "QuestionID": question.question_id,

                "Category": question.category,

                "Subcategory": question.subcategory,

                "Difficulty": question.difficulty,

                "QuestionType": question.question_type,

                "Question": question.question_text,

                "Answer": question.primary_answer,

                "AcceptedAnswers": question.accepted_answers,

                "RejectedAnswers": question.rejected_answers,

                "Validation": question.answer_validation,

                "Points": question.points,

                "Timer": question.timer_seconds,

                "Media": question.media_file,

                "Explanation": question.explanation,

                "HostNotes": question.host_notes,

                "Source": question.source_reference,

                "TimesAsked": question.times_asked,

                "TimesCorrect": question.times_correct,

                "TimesIncorrect": question.times_incorrect,

                "Active": question.active,

            }

        )

    dataframe = pd.DataFrame(rows)

    dataframe.to_excel(

        file_name,

        index=False,

    )

    return len(rows)


if __name__ == "__main__":

    total = export_excel(

        "exports/questions.xlsx"

    )

    print()

    print("Questions Exported")

    print("------------------")

    print(total)