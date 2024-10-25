from collections.abc import Callable

from .interview_manager_state import InterviewManagerState
from ..session.session_service import SessionService
from .start_state import InterviewManagerStartState
from ...domain.models.session import SessionStage

step_map: dict[SessionStage, Callable[..., InterviewManagerState]] = {
    SessionStage.START: InterviewManagerStartState,
}


class InterviewManager:
    def __init__(self, session_id: str, session_service: SessionService):
        self.ready = False
        self.session_id = session_id
        self.session_service = session_service
        self.state = None

    async def initialize(self):
        session = self.session_service.get_session(self.session_id)
        print(session)
        state = step_map[session["stage"]](session)
        self.change_state(state)

    def change_state(self, state: InterviewManagerState):
        self.state = state

    async def handle_message(self, message: str):
        if not self.ready:
            await self.initialize()
        response: str = await self.state.handle_message(message=message)
        print(response)
