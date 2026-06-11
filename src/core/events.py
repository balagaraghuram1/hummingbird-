"""Application lifecycle events.

Handles startup and shutdown events for database connections,
cache, and other services.
"""

from __future__ import annotations

import logging

from src.config.database import init_db

logger = logging.getLogger(__name__)


def register_events() -> None:
    """Register application lifecycle events.

    This function is called during application startup to
    initialize database tables and other services.
    """
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Database initialization failed: %s", e)
        raise
# v19 - updated 2026-06-11
# v49 - updated 2026-06-11
# v79 - updated 2026-06-11
# v109 - updated 2026-06-11
# v139 - updated 2026-06-11
