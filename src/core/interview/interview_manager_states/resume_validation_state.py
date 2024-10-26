from typing import Optional

from src.core.interview.interview_manager_states.job_description_state import InterviewManagerJobDescriptionState
from src.core.interview.interview_manager_states.state_base import InterviewManagerStateInterface, \
    InterviewManagerStateBase
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class InterviewManagerResumeValidationState(InterviewManagerStateInterface, InterviewManagerStateBase):
    def __init__(self, change_state, session):
        super().__init__(change_state=change_state, session=session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        # TODO: Resume validation message
        return Message(
            content="Resume validation feature is coming soon",
            type=MessageType.SYSTEM
        )

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.RESUME_VALIDATION

    async def handle_message(self, message: Optional[str]) -> Message:
        # TODO: Resume validation

        target_state = InterviewManagerJobDescriptionState(session=self.session, change_state=self.change_state)
        self.change_state(target_state)

        return target_state.get_init_message()
