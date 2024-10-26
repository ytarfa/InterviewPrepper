from typing import Optional, Callable

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.interview_manager_states.state_base import (
    InterviewManagerStateInterface,
    InterviewManagerStateBase,
)
from src.core.interview.interview_manager_states.job_description_state import (
    JobDescriptionState,
)
from src.core.interview.interview_manager_states.resume_state import ResumeState
from src.core.prompts.interview.introduction import (
    start_message_intent_classifier_prompt,
    StartMessageClassifierPromptOutput,
)
from src.domain.models.message import Message
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_haiku


change_state_map: dict[
    StartMessageClassifierPromptOutput, Callable[..., InterviewManagerStateInterface]
] = {
    StartMessageClassifierPromptOutput.RESUME: ResumeState,
    StartMessageClassifierPromptOutput.JOB_DESCRIPTION: JobDescriptionState,
    # TODO: Create state for 'other'
    StartMessageClassifierPromptOutput.OTHER: ResumeState,
}


class StartState(InterviewManagerStateInterface, InterviewManagerStateBase):
    def __init__(self, change_state, session):
        super().__init__(change_state=change_state, session=session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return None

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.JOB_DESCRIPTION

    async def handle_message(self, message: Optional[str]) -> Message:
        chain = (
            PromptTemplate.from_template(start_message_intent_classifier_prompt)
            | claude_haiku()
            | StrOutputParser()
        )
        response = chain.invoke({"message": message})
        # TODO: response should be casted to the enum and validated
        target_state = change_state_map[StartMessageClassifierPromptOutput(response)](
            session=self.session, change_state=self.change_state
        )
        self.change_state(target_state)
        # Return the init message of the target state
        return target_state.get_init_message()
