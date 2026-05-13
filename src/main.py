"""Hummingbird Medical AI application factory.

Creates and configures the FastAPI application with
all routes, middleware, and lifecycle events.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.api.main import api_router
from src.api.middleware import setup_middleware
from src.config.settings import settings
from src.utils.logger import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events for the application.
    """
    configure_logging(settings.log_level)
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)

    if settings.is_ai_configured:
        logger.info("AI provider configured: %s", settings.model_name)
    else:
        logger.warning("No AI provider configured. Running in offline mode.")

    yield

    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Production-ready medical AI system for diagnosis, "
            "treatment recommendations, and lab analysis."
        ),
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_middleware(app)
    app.include_router(api_router, prefix="/api")
    app.mount("/metrics", make_asgi_app())

    return app


app = create_app()
# v21 - updated 2026-06-11
# v51 - updated 2026-06-11
# v81 - updated 2026-06-11
