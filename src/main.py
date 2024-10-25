from dotenv import load_dotenv
from fastapi import FastAPI

from .api.sessions_routes import sessions_router

load_dotenv()
app = FastAPI(title="Interview Prepper API")
app.include_router(sessions_router)
