"""
==========================================================
TikTrivia Pro
Question Import Engine
Version 0.3.0
==========================================================
"""

from __future__ import annotations

import pandas as pd

from source.modules.questions.template_mapper import (
    STANDARD,
    TemplateMapper,
)

from source.services.question_service import add_question


def import_excel(

    file_name: str,

    mapping=STANDARD,

):

    mapper = TemplateMapper(mapping)

    dataframe = pd.read_excel(file_name)

    imported = 0

    errors = 0

    for _, row in dataframe.iterrows():

        try:

            add_question(

                question_id=str(

                    mapper.value(

                        row,

                        "QuestionID",

                    )

                ),

                category=str(

                    mapper.value(

                        row,

                        "Category",

                    )

                ),

                subcategory=str(

                    mapper.value(

                        row,

                        "Subcategory",

                    )

                ),

                difficulty=str(

                    mapper.value(

                        row,

                        "Difficulty",

                        "Intermediate",

                    )

                ),

                question_type=str(

                    mapper.value(

                        row,

                        "QuestionType",

                        "Standard",

                    )

                ),

                question_text=str(

                    mapper.value(

                        row,

                        "Question",

                    )

                ),

                primary_answer=str(

                    mapper.value(

                        row,

                        "Answer",

                    )

                ),

                accepted_answers=str(

                    mapper.value(

                        row,

                        "AcceptedAnswers",

                    )

                ),

                rejected_answers=str(

                    mapper.value(

                        row,

                        "RejectedAnswers",

                    )

                ),

                answer_validation=str(

                    mapper.value(

                        row,

                        "Validation",

                        "Exact",

                    )

                ),

                points=int(

                    mapper.value(

                        row,

                        "Points",

                        100,

                    )

                ),

                timer_seconds=int(

                    mapper.value(

                        row,

                        "Timer",

                        15,

                    )

                ),

                media_file=str(

                    mapper.value(

                        row,

                        "Media",

                    )

                ),

                explanation=str(

                    mapper.value(

                        row,

                        "Explanation",

                    )

                ),

                host_notes=str(

                    mapper.value(

                        row,

                        "HostNotes",

                    )

                ),

                source_reference=str(

                    mapper.value(

                        row,

                        "Source",

                    )

                ),

            )

            imported += 1

        except Exception:

            errors += 1

            continue

    return {

        "Imported": imported,

        "Errors": errors,

    }


if __name__ == "__main__":

    print()

    print("Question Import Engine Ready")

    print()