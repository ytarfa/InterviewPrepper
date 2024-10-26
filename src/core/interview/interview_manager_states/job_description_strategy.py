from typing import Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.interview_manager_states.job_description_validation_strategy import (
    JobDescriptionValidationStrategy,
)
from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
    SessionServiceAwareInterviewManagerStrategyBase,
)
from src.core.prompts.interview.extract_job_description_info import (
    extract_job_description_info_prompt_template,
)
from src.core.prompts.interview.introduction import get_job_description_message
from src.domain.models.job_description_info import JobDescriptionInfo
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_sonnet


class JobDescriptionStrategy(SessionServiceAwareInterviewManagerStrategyBase):
    def __init__(self, session, session_service):
        super().__init__(session=session, session_service=session_service)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(content=get_job_description_message, type=MessageType.SYSTEM)

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.JOB_DESCRIPTION

    async def handle_message(
        self, message: Optional[str]
    ) -> type[InterviewManagerStrategyInterface]:
        parser = PydanticOutputParser(pydantic_object=JobDescriptionInfo)
        format_instructions = parser.get_format_instructions()
        chain = (
            (
                PromptTemplate(
                    input_variables=["job_description_text"],
                    partial_variables={"format_instructions": format_instructions},
                    template=extract_job_description_info_prompt_template,
                )
            )
            | claude_sonnet()
            | parser
        )

        job_description_info: JobDescriptionInfo = chain.invoke(
            {"job_description_text": message}
        )

        # Save job description info to session
        # TODO: decouple state and TinyDBSessionService
        self.session_service.update_job_description_info(
            session_id=self.session.session_id,
            job_description_info=job_description_info,
        )

        return JobDescriptionValidationStrategy
