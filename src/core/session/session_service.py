import abc
from abc import ABC

from ...domain.models.interview_question import InterviewQuestion
from ...domain.models.job_description_info import JobDescriptionInfo
from ...domain.models.message import Message
from ...domain.models.resume_info import ResumeInfo
from ...domain.models.session import Session, SessionState


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

    @staticmethod
    @abc.abstractmethod
    def update_resume_info(session_id: str, resume_info: ResumeInfo):
        pass

    @staticmethod
    @abc.abstractmethod
    def update_job_description_info(
        session_id: str, job_description_info: JobDescriptionInfo
    ):
        pass

    @staticmethod
    @abc.abstractmethod
    def delete_all_sessions():
        pass

    @staticmethod
    @abc.abstractmethod
    def delete_session(session_id: str):
        pass

    @staticmethod
    @abc.abstractmethod
    def update_state(session_id: str, state: SessionState):
        pass

    @staticmethod
    @abc.abstractmethod
    def update_context_interview_question(
        session_id: str, interview_question: InterviewQuestion
    ):
        pass
