# api/routes.py
from fastapi import APIRouter

from ..core.session.tiny_db_session_service import TinyDBSessionService

sessions_router = APIRouter(prefix="/api/sessions")


@sessions_router.get("/")
async def get_all_sessions():
    session_service = TinyDBSessionService()
    return session_service.get_all_sessions()


@sessions_router.post("/")
async def create_session():
    session_service = TinyDBSessionService()
    return session_service.create_session()


@sessions_router.delete("/")
async def delete_all_sessions():
    session_service = TinyDBSessionService()
    return session_service.delete_all_sessions()


@sessions_router.get("/{session_id}")
async def get_session(session_id: str):
    session_service = TinyDBSessionService()
    return session_service.get_session(session_id)


@sessions_router.delete("/{session_id}")
async def delete_session(session_id: str):
    session_service = TinyDBSessionService()
    return session_service.delete_session(session_id)
