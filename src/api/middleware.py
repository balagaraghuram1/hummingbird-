import time

from fastapi import FastAPI, Request


def setup_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_timing(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
        return response

