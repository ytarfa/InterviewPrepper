from abc import ABC

from ...domain.models.session import Session


class SessionService(ABC):
    @staticmethod
    async def get_all_sessions() -> list[Session]:
        pass

    @staticmethod
    async def create_session() -> Session:
        pass

    @staticmethod
    async def get_session(session_id: str) -> Session:
        pass

    @staticmethod
    async def add_messages(session_id: str, messages: list[str]) -> Session:
        pass
