"""
==========================================================
TikTrivia Pro
Template Mapper
Version 0.3.0
==========================================================
"""

from __future__ import annotations


class TemplateMapper:

    def __init__(

        self,

        mapping: dict,

    ):

        self.mapping = mapping

    def value(

        self,

        row,

        field,

        default="",

    ):

        column = self.mapping.get(field)

        if column is None:

            return default

        if column not in row:

            return default

        value = row[column]

        if value is None:

            return default

        return value


STANDARD = {

    "QuestionID": "QuestionID",

    "Category": "Category",

    "Subcategory": "Subcategory",

    "Difficulty": "Difficulty",

    "QuestionType": "QuestionType",

    "Question": "Question",

    "Answer": "Answer",

    "AcceptedAnswers": "AcceptedAnswers",

    "RejectedAnswers": "RejectedAnswers",

    "Validation": "Validation",

    "Points": "Points",

    "Timer": "Timer",

    "Media": "Media",

    "Explanation": "Explanation",

    "HostNotes": "HostNotes",

    "Source": "Source",

}