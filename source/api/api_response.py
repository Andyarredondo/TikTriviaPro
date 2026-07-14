"""
==========================================================
TikTrivia Pro
Standard API Response
==========================================================
"""

from typing import Any

from fastapi.responses import JSONResponse


def success(
    data: Any = None,
    message: str = "",
    status_code: int = 200,
):
    """
    Standard success response.
    """

    return JSONResponse(

        status_code=status_code,

        content={

            "success": True,

            "message": message,

            "data": data,

        },

    )


def failure(
    message: str,
    status_code: int = 400,
    data: Any = None,
):
    """
    Standard failure response.
    """

    return JSONResponse(

        status_code=status_code,

        content={

            "success": False,

            "message": message,

            "data": data,

        },

    )