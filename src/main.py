from dotenv import load_dotenv
from fastapi import FastAPI

from .containers import Container

from src.api.sessions_routes import sessions_router


def create_app() -> FastAPI:
    load_dotenv()

    app = FastAPI(title="Interview Prepper API")
    container = Container()

    app.container = container

    app.include_router(sessions_router)

    return app


app = create_app()
