import os
from typing import Optional, Callable

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from .interview_manager_state import InterviewManagerState
from .job_description_state import InterviewManagerJobDescriptionState
from .resume_state import InterviewManagerResumeState
from ..prompts.interview.introduction import start_message_intent_classifier_prompt, \
    StartMessageClassifierPromptOutput
from ...domain.models.message import Message
from ...infrastructure.llm import claude_haiku


change_state_map: dict[StartMessageClassifierPromptOutput, Callable[..., InterviewManagerState]] = {
    StartMessageClassifierPromptOutput.RESUME: InterviewManagerResumeState,
    StartMessageClassifierPromptOutput.JOB_DESCRIPTION: InterviewManagerJobDescriptionState,
    # TODO: Create state for 'other'
    StartMessageClassifierPromptOutput.OTHER: InterviewManagerResumeState,
}

class InterviewManagerStartState(InterviewManagerState):
    def __init__(self, change_state, session):
        self.__change_state = change_state
        self.session = session

    def get_init_message(self) -> Optional[Message]:
        return None

    async def handle_message(self, message: Optional[str]) -> Message:
        chain = (PromptTemplate.from_template(start_message_intent_classifier_prompt)
                 | claude_haiku() | StrOutputParser())
        response = chain.invoke({
            "message": message
        })
        # TODO: response should be casted to the enum and validated
        target_state = change_state_map[StartMessageClassifierPromptOutput(response)](session=self.session, change_state=self.__change_state)
        self.__change_state(target_state)
        # Return the init message of the target state
        return target_state.get_init_message()
