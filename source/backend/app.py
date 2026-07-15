"""
==========================================================
TikTrivia Pro
Application Entry Point
Version: 0.4.0
==========================================================

Purpose
-------
Starts the TikTrivia Pro application.

Responsibilities
----------------
• Load configuration
• Configure logging
• Initialize the database
• Register API routers
• Serve HTML templates
• Serve static files
• Provide application health endpoint

Author
------
Andy Arredondo
"""

from __future__ import annotations

import json
import logging
import logging.config
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi import Request

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.api.contestants import router as contestant_router
from source.api.familyfeud import router as familyfeud_router
from source.api.questions import router as question_router
from source.api.productions import router as production_router
from source.backend.config import load_settings
from source.backend.database import Base
from source.backend.database import engine

# Register all SQLAlchemy models before create_all() runs.
import source.backend.familyfeud_models
import source.backend.models
import source.backend.production_models

# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIRECTORY = PROJECT_ROOT / "source" / "config"

FRONTEND_DIRECTORY = PROJECT_ROOT / "source" / "frontend"

STATIC_DIRECTORY = FRONTEND_DIRECTORY / "static"

TEMPLATE_DIRECTORY = FRONTEND_DIRECTORY / "templates"

LOGGING_CONFIGURATION = CONFIG_DIRECTORY / "logging.json"


# ----------------------------------------------------------
# Load Application Settings
# ----------------------------------------------------------

settings = load_settings()


# ----------------------------------------------------------
# Configure Logging
# ----------------------------------------------------------

with LOGGING_CONFIGURATION.open(
    "r",
    encoding="utf-8",
) as file:
    logging_configuration = json.load(file)

logging.config.dictConfig(logging_configuration)

logger = logging.getLogger("TikTriviaPro")


# ----------------------------------------------------------
# Application Startup / Shutdown
# ----------------------------------------------------------

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Run startup and shutdown operations.
    """

    logger.info("Starting TikTrivia Pro")

    Base.metadata.create_all(bind=engine)

    logger.info("Database initialized")

    yield

    logger.info("TikTrivia Pro shutdown complete")


# ----------------------------------------------------------
# FastAPI Application
# ----------------------------------------------------------

app = FastAPI(
    title=settings["application"]["name"],
    version=settings["application"]["version"],
    lifespan=lifespan,
)

# ----------------------------------------------------------
# React CORS
# ----------------------------------------------------------

app.add_middleware(

    CORSMiddleware,

  allow_origins=[

    "http://localhost:5173",

    "http://localhost:5174",

],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# ----------------------------------------------------------
# Register API Routers
# ----------------------------------------------------------

app.include_router(contestant_router)
app.include_router(question_router)
app.include_router(familyfeud_router)
app.include_router(production_router)


# ----------------------------------------------------------
# Static Files
# ----------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIRECTORY),
    name="static",
)


# ----------------------------------------------------------
# Templates
# ----------------------------------------------------------

templates = Jinja2Templates(
    directory=TEMPLATE_DIRECTORY,
)


# ----------------------------------------------------------
# Home Page
# ----------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):
    """
    Display the TikTrivia Pro host control panel.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "title": settings["application"]["name"],
            "version": settings["application"]["version"],
        },
    )


# ----------------------------------------------------------
# Health Check
# ----------------------------------------------------------

@app.get("/health")
async def health():
    """
    Return application health information.
    """

    return {
        "status": "healthy",
        "application": settings["application"]["name"],
        "version": settings["application"]["version"],
    }


# ----------------------------------------------------------
# Run Directly
# ----------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "source.backend.app:app",
        host=settings["server"]["host"],
        port=settings["server"]["port"],
        reload=True,
    )