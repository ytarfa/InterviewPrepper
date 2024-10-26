from typing import Annotated, Optional

from fastapi.params import Depends

from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from .strategy.strategy_factory import StrategyFactory
from ..session.session_service import SessionService
from ..session.tiny_db_session_service import TinyDBSessionService
from ...domain.models.message import Message, MessageType


class InterviewManager:
    def __init__(
        self,
        session_service: Annotated[SessionService, Depends(TinyDBSessionService)],
        strategy_factory: Annotated[StrategyFactory, Depends(StrategyFactory)],
    ):
        self.session_service = session_service
        self.strategy_factory = strategy_factory
        self.ready = False
        self.session_id = None
        self.strategy: Optional[InterviewManagerStrategyInterface] = None

    async def initialize(self, session_id: str):
        self.session_id = session_id
        session = self.session_service.get_session(session_id)
        self.strategy = self.strategy_factory.create_strategy(
            session_id=self.session_id, session_state=session.state
        )
        self.ready = True

    async def handle_message(self, message: str):
        if not self.ready:
            raise Exception("Interview Manager was not initialized correctly.")

        # Write user message to session messages
        self.session_service.add_messages(
            session_id=self.session_id,
            messages=[Message(content=message, type=MessageType.USER)],
        )

        strategy_commands = await self.strategy.handle_message(message=message)
        for command in strategy_commands:
            command.execute()
