from collections.abc import Callable

from .interview_manager_state import InterviewManagerState
from .job_description_state import InterviewManagerJobDescriptionState
from .resume_state import InterviewManagerResumeState
from ..session.session_service import SessionService
from .start_state import InterviewManagerStartState
from ...domain.models.message import Message, MessageType
from ...domain.models.session import SessionState

step_map: dict[SessionState, Callable[..., InterviewManagerState]] = {
    SessionState.START: InterviewManagerStartState,
    SessionState.RESUME: InterviewManagerResumeState,
    SessionState.JOB_DESCRIPTION: InterviewManagerJobDescriptionState
}


class InterviewManager:
    def __init__(self, session_id: str, session_service: SessionService):
        self.ready = False
        self.session_id = session_id
        self.session_service = session_service
        self.state = None

    async def initialize(self):
        session = self.session_service.get_session(self.session_id)
        state = step_map[session.state](change_state=self.change_state, session=session)
        self.change_state(state)

    def change_state(self, state: InterviewManagerState):
        self.session_service.change_state(self.session_id, state.get_session_state())
        self.state = state

    async def handle_message(self, message: str) -> Message:
        if not self.ready:
            await self.initialize()

        # Write user message to session messages
        self.session_service.add_messages(session_id=self.session_id, messages=[
            Message(
                content=message,
                type=MessageType.USER
            )
        ])
        # Handle message
        response = await self.state.handle_message(message=message)
        # Write response to session messages
        self.session_service.add_messages(session_id=self.session_id, messages=[response])
        return response
