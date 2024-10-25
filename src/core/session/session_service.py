import abc
from abc import ABC

from ...domain.models.message import Message
from ...domain.models.session import Session


class SessionService(ABC):
    @staticmethod
    @abc.abstractmethod
    def get_all_sessions() -> list[Session]:
        pass

    @staticmethod
    @abc.abstractmethod
    def create_session() -> Session:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_session(session_id: str) -> Session:
        pass

    @staticmethod
    @abc.abstractmethod
    def add_messages(session_id: str, messages: list[Message]) -> Session:
        pass
