import uuid
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from dataclasses import dataclass
from abc import ABC


db = TinyDB('../session-db.json', storage=CachingMiddleware(JSONStorage))


@dataclass
class Session:
    session_id: str
    resume: str = None
    job_description: str = None
    resume_skills: list = None
    job_description_skills: list = None
    yoe: int = None
    messages: list = None


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
        db.insert(session.__dict__)
        return session

    @staticmethod
    def get_session(session_id: str) -> Session:
        return db.get(doc_id=session_id)

    @staticmethod
    def add_messages(session_id: str, messages: list[str]) -> Session:
        session: Session = db.get(doc_id=session_id)
        session.messages.append(messages)
        return session
