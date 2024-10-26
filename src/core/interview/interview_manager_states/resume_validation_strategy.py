from typing import Optional

from src.core.interview.interview_manager_states.job_description_strategy import (
    JobDescriptionStrategy,
)
from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class ResumeValidationStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        # TODO: Resume validation message
        return Message(
            content="Resume validation feature is coming soon", type=MessageType.SYSTEM
        )

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.RESUME_VALIDATION

    async def handle_message(
        self, message: Optional[str]
    ) -> type[InterviewManagerStrategyInterface]:
        # TODO: Resume validation
        return JobDescriptionStrategy
