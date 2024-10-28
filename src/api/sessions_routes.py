from typing import Optional, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.containers import Container
from src.core.interview.interview_manager import InterviewManager
from src.core.interview.interview_message_context import InterviewMessageContext
from src.core.session.session_service import SessionService
from src.domain.models.message import Message

sessions_router = APIRouter(prefix="/api/sessions")


@sessions_router.get("/")
@inject
async def get_all_sessions(
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    return session_service.get_all_sessions()


@sessions_router.post("/")
@inject
async def create_session(
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    return session_service.create_session()


@sessions_router.delete("/")
@inject
async def delete_all_sessions(
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    return session_service.delete_all_sessions()


@sessions_router.get("/{session_id}")
@inject
def get_session(
    session_id: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    return session_service.get_session(session_id)


@sessions_router.delete("/{session_id}")
@inject
async def delete_session(
    session_id: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    return session_service.delete_session(session_id)


class HandleMessageData(BaseModel):
    session_id: str
    message: Optional[str] = None


@sessions_router.post("/message")
@inject
async def handle_message(
    data: HandleMessageData,
    interview_manager: InterviewManager = Depends(Provide[Container.interview_manager]),
    interview_message_context: InterviewMessageContext = Depends(
        Provide[Container.interview_message_context]
    ),
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> list[Message]:
    await interview_manager.initialize(data.session_id)
    await interview_manager.handle_message(data.message)
    messages = interview_message_context.get_messages()
    interview_message_context.clear_messages()
    session_service.add_messages(session_id=data.session_id, messages=messages)
    return messages
