from typing import Optional

from dependency_injector.providers import Callable

from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from ..session.session_service import SessionService
from ...domain.models.message import Message, MessageType
from ...domain.models.session import SessionState


class InterviewManager:
    def __init__(
        self,
        session_service: SessionService,
        strategy_providers: dict[
            SessionState, Callable[..., InterviewManagerStrategyInterface]
        ],
    ):
        self.session_service = session_service
        self.ready = False
        self.session_id = None
        self.strategy: Optional[InterviewManagerStrategyInterface] = None
        self.strategy_providers = strategy_providers

    async def initialize(self, session_id: str):
        self.session_id = session_id
        session = self.session_service.get_session(session_id)
        self.strategy = self.strategy_providers.get(session.state)(
            session_id=self.session_id
        )
        self.ready = True

    async def handle_message(self, message: str):
        if not self.ready:
            raise Exception("Interview Manager was not initialized.")

        # Write user message to session messages
        self.session_service.add_messages(
            session_id=self.session_id,
            messages=[Message(content=message, type=MessageType.USER)],
        )

        strategy_commands = await self.strategy.handle_message(message=message)
        for command in strategy_commands:
            command.execute()
