from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.session.session_service import SessionService
from src.domain.models.resume_info import ResumeInfo


class UpdateSessionResumeInfoCommand(InterviewCommand):
    def __init__(
        self, session_service: SessionService, session_id: str, resume_info: ResumeInfo
    ):
        self.session_service = session_service
        self.session_id = session_id
        self.resume_info = resume_info

    def execute(self):
        self.session_service.update_resume_info(
            session_id=self.session_id, resume_info=self.resume_info
        )
