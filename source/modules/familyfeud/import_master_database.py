"""
==========================================================
TikTrivia Pro
Import Friendly Feud Master Database
==========================================================
"""

from source.modules.familyfeud.familyfeud_validator import (
    validate_workbook,
)

from source.modules.familyfeud.familyfeud_importer import (
    import_workbook,
)


WORKBOOK = r"imports\FriendlyFeud_Master_Database_v3.0.xlsx"


if __name__ == "__main__":

    report = validate_workbook(

        WORKBOOK

    )

    print(report)

    if report["valid"]:

        print()

        print("Importing...")

        print()

        result = import_workbook(

            WORKBOOK

        )

        print(result)

    else:

        print()

        print("Workbook validation failed.")