from typing import Annotated

from src.core.interview.strategy.answer_evaluation_strategy import (
    AnswerEvaluationStrategy,
)
from src.core.interview.strategy.interview_question_strategy import (
    InterviewQuestionStrategy,
)
from src.core.interview.strategy.job_description_strategy import (
    JobDescriptionStrategy,
)
from src.core.interview.strategy.resume_strategy import (
    ResumeStrategy,
)
from src.core.interview.strategy.start_strategy import (
    StartStrategy,
)
from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.interview.interview_message_context import InterviewMessageContext
from src.core.session.session_service import SessionService
from src.domain.models.session import SessionState

SESSION_STATE_STRATEGY_MAP: dict[
    SessionState,
    type[InterviewManagerStrategyInterface],
] = {
    SessionState.START: StartStrategy,
    SessionState.RESUME: ResumeStrategy,
    SessionState.JOB_DESCRIPTION: JobDescriptionStrategy,
    SessionState.INTERVIEW: InterviewQuestionStrategy,
    SessionState.EVALUATION: AnswerEvaluationStrategy,
}


class StrategyFactory:
    def __init__(
        self,
        session_service: SessionService,
        interview_message_context: InterviewMessageContext,
    ):
        self.session_service = session_service
        self.interview_message_context = interview_message_context

    def create_strategy(
        self, session_id: str, session_state: SessionState
    ) -> InterviewManagerStrategyInterface:
        target_state = SESSION_STATE_STRATEGY_MAP[session_state]
        session = self.session_service.get_session(session_id=session_id)
        return target_state(
            session=session,
            session_service=self.session_service,
            interview_message_context=self.interview_message_context,
        )
