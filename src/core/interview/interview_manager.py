from collections.abc import Callable

from .interview_manager_states.interview_state import InterviewState
from .interview_manager_states.job_description_state import JobDescriptionState
from .interview_manager_states.job_description_validation_state import JobDescriptionValidationState
from .interview_manager_states.resume_state import ResumeState
from .interview_manager_states.resume_validation_state import ResumeValidationState
from .interview_manager_states.start_state import StartState
from .interview_manager_states.state_base import InterviewManagerStateInterface
from ..session.session_service import SessionService
from ...domain.models.message import Message, MessageType
from ...domain.models.session import SessionState

step_map: dict[SessionState, Callable[..., InterviewManagerStateInterface]] = {
    SessionState.START: StartState,
    SessionState.RESUME: ResumeState,
    SessionState.JOB_DESCRIPTION: JobDescriptionState,
    SessionState.RESUME_VALIDATION: ResumeValidationState,
    SessionState.JOB_DESCRIPTION_VALIDATION: JobDescriptionValidationState,
    SessionState.INTERVIEW: InterviewState
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

    def change_state(self, state: InterviewManagerStateInterface):
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
