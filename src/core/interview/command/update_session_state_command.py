from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.session.session_service import SessionService
from src.domain.models.session import SessionState


class UpdateSessionStateCommand(InterviewCommand):
    def __init__(
        self,
        session_id: str,
        session_service: SessionService,
        target_state: SessionState,
    ):
        self.session_id = session_id
        self.session_service = session_service
        self.target_state = target_state

    def execute(self):
        self.session_service.update_state(self.session_id, self.target_state)
