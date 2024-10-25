from fastapi import FastAPI

from .api.sessions_routes import sessions_router

app = FastAPI(title="Interview Prepper API")
app.include_router(sessions_router)
