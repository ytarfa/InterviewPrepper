from abc import ABC

from ...domain.models.session import Session


class SessionService(ABC):
    def get_all_sessions(self) -> list[Session]:
        pass

    def create_session(self) -> Session:
        pass

    def get_session(self, session_id: str) -> Session:
        pass

    def add_messages(self, session_id: str, messages: list[str]) -> Session:
        pass
