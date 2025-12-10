"""HTTP middleware for request processing.

Provides timing, logging, and metrics middleware
for API request monitoring.
"""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.monitoring import REQUEST_COUNT, REQUEST_LATENCY

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware that adds request timing headers and metrics."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        response.headers["X-Process-Time"] = f"{duration:.4f}"
        response.headers["X-Request-ID"] = request_id

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        if duration > 1.0:
            logger.warning(
                "Slow request: %s %s took %.2fs",
                request.method,
                request.url.path,
                duration,
            )

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs request/response details."""

    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(
            "Request: %s %s from %s",
            request.method,
            request.url.path,
            request.client.host if request.client else "unknown",
        )

        response = await call_next(request)

        logger.info(
            "Response: %s %s -> %d",
            request.method,
            request.url.path,
            response.status_code,
        )

        return response


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware for the application.

    Args:
        app: FastAPI application instance.
    """
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)
