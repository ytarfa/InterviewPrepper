import abc
from abc import ABC
from typing import Optional, Annotated

from fastapi.params import Depends
from typing_extensions import Self

from src.core.session.session_service import SessionService
from src.core.session.tiny_db_session_service import TinyDBSessionService
from src.domain.models.message import Message
from src.domain.models.session import Session, SessionState


class InterviewManagerStrategyInterface(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abc.abstractmethod
    async def handle_message(self, message: Optional[str]) -> type[Self]:
        """Handles the message and returns the target state"""
        pass

    @staticmethod
    @abc.abstractmethod
    def get_init_message() -> Optional[Message]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_session_state() -> SessionState:
        pass


class SessionServiceAwareInterviewManagerStrategyBase(
    InterviewManagerStrategyInterface, ABC
):
    def __init__(
        self,
        session: Session,
        session_service: Annotated[SessionService, Depends(TinyDBSessionService)],
    ):
        super().__init__(session=session)
        self.session_service = session_service
