"""
==========================================================
TikTrivia Pro
Application Entry Point
Version: 0.1.0
==========================================================

Purpose
-------
Starts the TikTrivia Pro web application.

Responsibilities
----------------
• Load configuration
• Configure logging
• Initialize database
• Serve static files
• Serve HTML templates
• Provide health endpoint

Author
------
Andy Arredondo / TikTrivia Pro
"""

from __future__ import annotations

import json
import logging
import logging.config
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.backend.config import load_settings
from source.backend.database import Base, engine


# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIRECTORY = PROJECT_ROOT / "source" / "config"

FRONTEND_DIRECTORY = PROJECT_ROOT / "source" / "frontend"

TEMPLATES_DIRECTORY = FRONTEND_DIRECTORY / "templates"

STATIC_DIRECTORY = FRONTEND_DIRECTORY / "static"

LOGGING_FILE = CONFIG_DIRECTORY / "logging.json"


# ---------------------------------------------------------
# Load Configuration
# ---------------------------------------------------------

settings = load_settings()


# ---------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------

with LOGGING_FILE.open(
    "r",
    encoding="utf-8"
) as file:

    logging_configuration = json.load(file)

logging.config.dictConfig(logging_configuration)

logger = logging.getLogger("TikTriviaPro")


# ---------------------------------------------------------
# Application Startup
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting TikTrivia Pro")

    Base.metadata.create_all(bind=engine)

    logger.info("Database Initialized")

    yield

    logger.info("TikTrivia Pro Shutdown")


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(

    title=settings["application"]["name"],

    version=settings["application"]["version"],

    lifespan=lifespan
)


# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------

app.mount(

    "/static",

    StaticFiles(directory=STATIC_DIRECTORY),

    name="static"
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(

    directory=TEMPLATES_DIRECTORY
)


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)

async def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={

            "request": request,

            "title": settings["application"]["name"],

            "version": settings["application"]["version"]
        }
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")

async def health():

    return {

        "status": "healthy",

        "application": settings["application"]["name"],

        "version": settings["application"]["version"]
    }