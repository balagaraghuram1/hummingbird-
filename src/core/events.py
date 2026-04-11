from fastapi import FastAPI


def register_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup_event() -> None:
        return None

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        return None

