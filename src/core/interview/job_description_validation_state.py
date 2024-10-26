from typing import Optional

from src.core.interview.interview_manager_state import InterviewManagerStateInterface, InterviewManagerStateBase
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class InterviewManagerJobDescriptionValidationState(InterviewManagerStateInterface, InterviewManagerStateBase):
    def __init__(self, change_state, session):
        super().__init__(change_state=change_state, session=session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        # TODO: Job Description validation message
        return Message(
            content="",
            type=MessageType.SYSTEM
        )

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.JOB_DESCRIPTION_VALIDATION

    async def handle_message(self, message: Optional[str]) -> Message:
        pass