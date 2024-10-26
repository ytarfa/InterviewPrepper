from typing import Optional, Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

from ..core.interview.interview_manager import InterviewManager
from ..core.session.session_service import SessionService
from ..core.session.tiny_db_session_service import TinyDBSessionService
from ..domain.models.message import Message

sessions_router = APIRouter(prefix="/api/sessions")


@sessions_router.get("/")
async def get_all_sessions(
    session_service: Annotated[SessionService, Depends(TinyDBSessionService)]
):
    return session_service.get_all_sessions()


@sessions_router.post("/")
async def create_session(
    session_service: Annotated[SessionService, Depends(TinyDBSessionService)]
):
    return session_service.create_session()


@sessions_router.delete("/")
async def delete_all_sessions(
    session_service: Annotated[SessionService, Depends(TinyDBSessionService)]
):
    return session_service.delete_all_sessions()


@sessions_router.get("/{session_id}")
def get_session(
    session_id: str,
    session_service: Annotated[SessionService, Depends(TinyDBSessionService)],
):
    return session_service.get_session(session_id)


@sessions_router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    session_service: Annotated[SessionService, Depends(TinyDBSessionService)],
):
    return session_service.delete_session(session_id)


class HandleMessageData(BaseModel):
    session_id: str
    message: Optional[str] = None


@sessions_router.post("/message")
async def handle_message(
    data: HandleMessageData,
    interview_manager: Annotated[InterviewManager, Depends(InterviewManager)],
) -> Message:
    await interview_manager.initialize(data.session_id)
    return await interview_manager.handle_message(data.message)
