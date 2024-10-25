import uuid
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from abc import ABC

from ..types.session import Session


db = TinyDB('../session-db.json')


class SessionService(ABC):
    def get_all_sessions(self) -> list[Session]:
        pass

    def create_session(self) -> Session:
        pass

    def get_session(self, session_id: str) -> Session:
        pass

    def add_messages(self, session_id: str, messages: list[str]) -> Session:
        pass


class TinyDBSessionService:

    @staticmethod
    def get_all_sessions() -> list[Session]:
        return db.all()

    @staticmethod
    def create_session() -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id)
        session.messages = []
        db.insert(session.__dict__)
        return session

    @staticmethod
    def get_session(session_id: str) -> Session:
        Session = Query()
        return db.get(Session.session_id == session_id)

    @staticmethod
    def delete_session(session_id: str) -> None:
        Session = Query()
        db.remove(Session.session_id == session_id)

    @staticmethod
    def delete_all_sessions() -> None:
        sessions = db.all()
        Session = Query()
        for session in sessions:
            db.remove(Session.session_id == session["session_id"])
    @staticmethod
    def add_messages(session_id: str, messages: list[str]) -> Session:
        session: Session = db.get(doc_id=session_id)
        session.messages.append(messages)
        return session
