from typing import Optional, Callable, Tuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.interview.interview_manager_states.job_description_strategy import (
    JobDescriptionStrategy,
)
from src.core.interview.interview_manager_states.resume_strategy import ResumeStrategy
from src.core.prompts.interview.introduction import (
    start_message_intent_classifier_prompt,
    StartMessageClassifierPromptOutput,
)
from src.domain.models.message import Message
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_haiku


target_state_map: dict[
    StartMessageClassifierPromptOutput, type[InterviewManagerStrategyInterface]
] = {
    StartMessageClassifierPromptOutput.RESUME: ResumeStrategy,
    StartMessageClassifierPromptOutput.JOB_DESCRIPTION: JobDescriptionStrategy,
    # TODO: Create state for 'other'
    StartMessageClassifierPromptOutput.OTHER: ResumeStrategy,
}


class StartStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session):
        super().__init__(session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return None

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.JOB_DESCRIPTION

    async def handle_message(
        self, message: Optional[str]
    ) -> type[InterviewManagerStrategyInterface]:
        chain = (
            PromptTemplate.from_template(start_message_intent_classifier_prompt)
            | claude_haiku()
            | StrOutputParser()
        )
        response = chain.invoke({"message": message})
        # TODO: response should be casted to the enum and validated
        return target_state_map[StartMessageClassifierPromptOutput(response)]
