"""
==========================================================
TikTrivia Pro
Friendly Feud Workbook Validator
Version 0.3.0
==========================================================
"""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [

    "Board ID",

    "Category",

    "Survey Question",

    "Answer 1",

]


SHEET_NAME = "Publishing Master"


def validate_workbook(filename: str):

    report = {

        "valid": True,

        "errors": [],

        "warnings": [],

    }

    workbook = pd.ExcelFile(filename)

    if SHEET_NAME not in workbook.sheet_names:

        report["valid"] = False

        report["errors"].append(

            f'Missing worksheet "{SHEET_NAME}"'

        )

        return report

    dataframe = pd.read_excel(

        filename,

        sheet_name=SHEET_NAME,

    )

    # ------------------------------------

    # Required Columns

    # ------------------------------------

    for column in REQUIRED_COLUMNS:

        if column not in dataframe.columns:

            report["valid"] = False

            report["errors"].append(

                f"Missing column: {column}"

            )

    if not report["valid"]:

        return report

    # ------------------------------------

    # Duplicate Board IDs

    # ------------------------------------

    duplicates = dataframe[

        dataframe["Board ID"].duplicated()

    ]

    if len(duplicates):

        report["warnings"].append(

            f"{len(duplicates)} duplicate Board IDs"

        )

    # ------------------------------------

    # Missing Questions

    # ------------------------------------

    missing_questions = dataframe[

        dataframe["Survey Question"].isna()

    ]

    if len(missing_questions):

        report["warnings"].append(

            f"{len(missing_questions)} missing questions"

        )

    # ------------------------------------

    # Missing Answers

    # ------------------------------------

    missing_answers = dataframe[

        dataframe["Answer 1"].isna()

    ]

    if len(missing_answers):

        report["warnings"].append(

            f"{len(missing_answers)} boards missing Answer 1"

        )

    # ------------------------------------

    # Empty Categories

    # ------------------------------------

    missing_category = dataframe[

        dataframe["Category"].isna()

    ]

    if len(missing_category):

        report["warnings"].append(

            f"{len(missing_category)} missing categories"

        )

    report["rows"] = len(dataframe)

    report["columns"] = len(dataframe.columns)

    return report


if __name__ == "__main__":

    print()

    print("Friendly Feud Validator Ready")

    print()