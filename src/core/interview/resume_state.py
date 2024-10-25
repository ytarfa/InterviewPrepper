from typing import Optional

from src.core.interview.interview_manager_state import InterviewManagerState
from src.core.prompts.interview.introduction import get_resume_message
from src.domain.models.message import Message, MessageType


class InterviewManagerResumeState(InterviewManagerState):
    def __init__(self, change_state, session):
        super().__init__(session=session, change_state=change_state)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(
            content=get_resume_message,
            type=MessageType.SYSTEM
        )

    def handle_message(self, message: Optional[str]):
        pass