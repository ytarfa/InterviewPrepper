from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.session.session_service import SessionService
from src.domain.models.job_description_info import JobDescriptionInfo


class UpdateSessionJobDescriptionInfoCommand(InterviewCommand):
    def __init__(
        self,
        session_service: SessionService,
        session_id: str,
        job_description_info: JobDescriptionInfo,
    ):
        self.session_service = session_service
        self.session_id = session_id
        self.job_description_info = job_description_info

    def execute(self):
        self.session_service.update_job_description_info(
            session_id=self.session_id, job_description_info=self.job_description_info
        )
