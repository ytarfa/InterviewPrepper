from typing import Optional

from src.core.interview.interview_manager_states.interview_strategy import (
    InterviewStrategy,
)
from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class JobDescriptionValidationStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        # TODO: Job Description validation message
        return Message(content="", type=MessageType.SYSTEM)

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.JOB_DESCRIPTION_VALIDATION

    async def handle_message(
        self, message: Optional[str]
    ) -> type[InterviewManagerStrategyInterface]:
        # TODO: Job Description validation
        return InterviewStrategy
