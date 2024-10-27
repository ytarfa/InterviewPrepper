from src.core.interview.command.command_base import InterviewCommand
from src.core.session.session_service import SessionService
from src.domain.models.interview_question import InterviewQuestion


class UpdateSessionContextInterviewQuestionCommand(InterviewCommand):
    def __init__(
        self,
        session_id: str,
        interview_question: InterviewQuestion,
        session_service: SessionService,
    ):
        self.session_id = session_id
        self.interview_question = interview_question
        self.session_service = session_service

    def execute(self):
        self.session_service.update_context_interview_question(
            session_id=self.session_id, interview_question=self.interview_question
        )
