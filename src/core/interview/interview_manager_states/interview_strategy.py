from typing import Optional

from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState


class InterviewStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(content="", type=MessageType.SYSTEM)

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.INTERVIEW

    async def handle_message(
        self, message: Optional[str]
    ) -> type[InterviewManagerStrategyInterface]:
        pass
