import uuid
from tinydb import Query

from .session_service import SessionService
from ...domain.models.job_description_info import JobDescriptionInfo
from ...domain.models.message import Message
from ...domain.models.resume_info import ResumeInfo
from ...infrastructure.tiny_db import db
from ...domain.models.session import Session, SessionState


class TinyDBSessionService(SessionService):

    @staticmethod
    def get_all_sessions() -> list[Session]:
        return db.all()

    @staticmethod
    def create_session() -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id)
        db.insert(session.model_dump())
        return session

    @staticmethod
    def get_session(session_id: str) -> Session:
        session_query = Query()
        session_document = db.get(session_query.session_id == session_id)
        if session_document:
            return Session(**session_document)

    @staticmethod
    def delete_session(session_id: str) -> None:
        session_query = Query()
        db.remove(session_query.session_id == session_id)

    @staticmethod
    def delete_all_sessions() -> None:
        sessions = db.all()
        session_query = Query()
        for session_doc in sessions:
            db.remove(session_query.session_id == session_doc["session_id"])

    @staticmethod
    def add_messages(session_id: str, messages: list[Message]) -> Session:
        session_query = Query()
        session_document = db.get(session_query.session_id == session_id)
        if session_document:
            session = Session(**session_document)
            session.messages.extend(messages)
            db.update(session.model_dump(), session_query.session_id == session_id)
            return session

    @staticmethod
    def change_state(session_id: str, state: SessionState):
        session_query = Query()
        session_document = db.get(session_query.session_id == session_id)
        if session_document:
            session = Session(**session_document)
            session.state = state
            db.update(session.model_dump(), session_query.session_id == session_id)
            return session

    @staticmethod
    def update_resume_info(session_id: str, resume_info: ResumeInfo):
        session_query = Query()
        session_document = db.get(session_query.session_id == session_id)
        if session_document:
            session = Session(**session_document)
            session.resume_info = resume_info
            db.update(session.model_dump(), session_query.session_id == session_id)
            return session

    @staticmethod
    def update_job_description_info(session_id: str, job_description_info: JobDescriptionInfo):
        session_query = Query()
        session_document = db.get(session_query.session_id == session_id)
        if session_document:
            session = Session(**session_document)
            session.job_description_info = job_description_info
            db.update(session.model_dump(), session_query.session_id == session_id)
            return session
