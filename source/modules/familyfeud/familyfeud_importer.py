"""
==========================================================
TikTrivia Pro
Friendly Feud Importer
Version 0.3.0
==========================================================
"""

from __future__ import annotations

import pandas as pd

from source.backend.familyfeud_models import (
    FamilyFeudBoard,
    FamilyFeudAnswer,
)

from source.backend.session import (
    get_session,
    close_session,
)

from source.repositories.familyfeud_repository import (
    create_board,
    create_answer,
    get_board_by_code,
)


SHEET_NAME = "Publishing Master"


def import_workbook(filename: str):

    dataframe = pd.read_excel(
        filename,
        sheet_name=SHEET_NAME,
    )

    session = get_session()

    imported_boards = 0
    imported_answers = 0
    skipped = 0

    try:

        for _, row in dataframe.iterrows():

            board_code = str(row["Board ID"]).strip()

            if get_board_by_code(session, board_code):

                skipped += 1
                continue

            board = FamilyFeudBoard(

                board_id=board_code,

                category=str(row["Category"]),

                difficulty=str(row.get("Difficulty", "Intermediate")),

                energy=str(row.get("Energy", "Medium")),

                play_time=60,

                survey_question=str(row["Survey Question"]),

                host_opening=str(row.get("Host Opening", "")),

                talking_points=str(row.get("Host Talking Points", "")),

                hint1=str(row.get("Hint 1", "")),

                hint2=str(row.get("Hint 2", "")),

                reveal_script=str(row.get("Reveal Script", "")),

                audience_poll=str(row.get("Audience Poll", "")),

                chat_challenge=str(row.get("Chat Challenge", "")),

                viewer_story_prompt=str(row.get("Viewer Story Prompt", "")),

                interesting_fact=str(row.get("Interesting Fact", "")),

                little_known_fact=str(row.get("Little-Known Fact", "")),

                historical_note=str(row.get("Historical Note", "")),

                bonus_trivia=str(row.get("Bonus Trivia", "")),

                tie_breaker=str(row.get("Tie-Breaker", "")),

                moderator_notes=str(row.get("Moderator Notes", "")),

                production_notes=str(row.get("Production Notes", "")),

                tags=str(row.get("Tags", "")),

                source_reference=str(row.get("Source", "")),

                verification=str(row.get("Verification", "")),

                version=str(row.get("Version", "1.0")),

                last_reviewed=str(row.get("Last Reviewed", "")),
            )

            board = create_board(
                session,
                board,
            )

            imported_boards += 1

            for i in range(1, 11):

                answer_column = f"Answer {i}"

                if answer_column not in row:
                    continue

                answer = str(row[answer_column]).strip()

                if answer == "" or answer.lower() == "nan":
                    continue

                alternate = ""

                reject = ""

                alt_column = f"Alternate Acceptable Answers {i}"

                reject_column = f"Reject Answers {i}"

                if alt_column in row:
                    alternate = str(row[alt_column])

                if reject_column in row:
                    reject = str(row[reject_column])

                create_answer(

                    session,

                    FamilyFeudAnswer(

                        board_id=board.id,

                        rank=i,

                        answer=answer,

                        alternate_answers=alternate,

                        reject_answers=reject,

                        points=max(11 - i, 1),

                    ),

                )

                imported_answers += 1

        return {

            "Boards Imported": imported_boards,

            "Answers Imported": imported_answers,

            "Skipped": skipped,

        }

    finally:

        close_session(session)


if __name__ == "__main__":

    print()

    print("Friendly Feud Importer Ready")

    print()