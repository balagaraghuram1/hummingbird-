from fastapi import FastAPI
from prometheus_client import make_asgi_app

from src.api.main import api_router
from src.api.middleware import setup_middleware
from src.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    setup_middleware(app)
    app.include_router(api_router, prefix="/api")
    app.mount("/metrics", make_asgi_app())
    return app


app = create_app()

