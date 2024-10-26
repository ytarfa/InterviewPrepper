import abc
from abc import ABC
from collections.abc import Callable
from typing import Optional
from typing_extensions import Self

from ...domain.models.message import Message
from ...domain.models.session import Session, SessionState


class InterviewManagerStateBase:
    def __init__(self, change_state: Callable[Self, None], session: Session):
        self.change_state = change_state
        self.session = session


class InterviewManagerStateInterface(ABC):
    @abc.abstractmethod
    async def handle_message(self, message: Optional[str]) -> Message:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_init_message() -> Optional[Message]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_session_state() -> SessionState:
        pass