from typing import Optional

from src.core.interview.interview_manager_state import InterviewManagerState
from src.core.prompts.interview.introduction import get_job_description_message
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class InterviewManagerJobDescriptionState(InterviewManagerState):
    def __init__(self, change_state, session):
        super().__init__(session=session, change_state=change_state)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(
            content=get_job_description_message,
            type=MessageType.SYSTEM
        )

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.JOB_DESCRIPTION

    def handle_message(self, message: Optional[str]):
        pass