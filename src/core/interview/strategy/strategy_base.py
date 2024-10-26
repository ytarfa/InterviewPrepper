import abc
from abc import ABC
from typing import Optional

from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.interview.interview_message_context import InterviewMessageContext
from src.core.session.session_service import SessionService
from src.domain.models.message import Message
from src.domain.models.session import Session, SessionState


class InterviewManagerStrategyInterface(ABC):
    def __init__(
        self,
        session: Session,
        interview_message_context: InterviewMessageContext,
        session_service: SessionService,
    ):
        self.session = session
        self.session_service = session_service
        self.interview_message_context = interview_message_context

    @abc.abstractmethod
    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_init_message() -> Optional[Message]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_session_state() -> SessionState:
        pass
