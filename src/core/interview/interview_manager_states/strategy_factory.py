from typing import Annotated, Union

from fastapi.params import Depends

from src.core.interview.interview_manager_states.interview_strategy import (
    InterviewStrategy,
)
from src.core.interview.interview_manager_states.job_description_strategy import (
    JobDescriptionStrategy,
)
from src.core.interview.interview_manager_states.job_description_validation_strategy import (
    JobDescriptionValidationStrategy,
)
from src.core.interview.interview_manager_states.resume_strategy import ResumeStrategy
from src.core.interview.interview_manager_states.resume_validation_strategy import (
    ResumeValidationStrategy,
)
from src.core.interview.interview_manager_states.start_strategy import StartStrategy
from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
    SessionServiceAwareInterviewManagerStrategyBase,
)
from src.core.session.session_service import SessionService
from src.core.session.tiny_db_session_service import TinyDBSessionService
from src.domain.models.session import SessionState, Session

step_map: dict[
    SessionState,
    type[
        Union[
            InterviewManagerStrategyInterface,
            SessionServiceAwareInterviewManagerStrategyBase,
        ]
    ],
] = {
    SessionState.START: StartStrategy,
    SessionState.RESUME: ResumeStrategy,
    SessionState.JOB_DESCRIPTION: JobDescriptionStrategy,
    SessionState.RESUME_VALIDATION: ResumeValidationStrategy,
    SessionState.JOB_DESCRIPTION_VALIDATION: JobDescriptionValidationStrategy,
    SessionState.INTERVIEW: InterviewStrategy,
}


class StrategyFactory:
    def __init__(
        self, session_service: Annotated[SessionService, Depends(TinyDBSessionService)]
    ):
        self.session_service = session_service

    def create_strategy(self, session_id: str, session_state: SessionState) -> Union[
        InterviewManagerStrategyInterface,
        SessionServiceAwareInterviewManagerStrategyBase,
    ]:
        target_state = step_map[session_state]
        session = self.session_service.get_session(session_id=session_id)
        if issubclass(target_state, SessionServiceAwareInterviewManagerStrategyBase):
            return target_state(session=session, session_service=self.session_service)
        else:
            return target_state(session=session)
