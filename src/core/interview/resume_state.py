from typing import Optional

from src.core.interview.interview_manager_state import InterviewManagerStateInterface, InterviewManagerStateBase
from src.core.prompts.interview.introduction import get_resume_message
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class InterviewManagerResumeState(InterviewManagerStateInterface, InterviewManagerStateBase):
    def __init__(self, change_state, session):
        super().__init__(change_state=change_state, session=session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(
            content=get_resume_message,
            type=MessageType.SYSTEM
        )

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.RESUME

    def handle_message(self, message: Optional[str]):
        pass