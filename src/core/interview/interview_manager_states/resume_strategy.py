from typing import Optional, Annotated

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.interview_manager_states.strategy_base import (
    InterviewManagerStrategyInterface,
    SessionServiceAwareInterviewManagerStrategyBase,
)
from src.core.interview.interview_manager_states.resume_validation_strategy import (
    ResumeValidationStrategy,
)
from src.core.prompts.interview.extract_resume_info import (
    extract_resume_info_prompt_template,
)
from src.core.prompts.interview.introduction import get_resume_message
from src.domain.models.message import Message, MessageType
from src.domain.models.resume_info import ResumeInfo
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_sonnet


class ResumeStrategy(SessionServiceAwareInterviewManagerStrategyBase):
    def __init__(self, session, session_service):
        super().__init__(session=session, session_service=session_service)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(content=get_resume_message, type=MessageType.SYSTEM)

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.RESUME

    async def handle_message(
        self, message: Optional[str]
    ) -> type[InterviewManagerStrategyInterface]:
        parser = PydanticOutputParser(pydantic_object=ResumeInfo)
        format_instructions = parser.get_format_instructions()
        extract_resume_info_chain = (
            (
                PromptTemplate(
                    input_variables=["resume_text"],
                    partial_variables={"format_instructions": format_instructions},
                    template=extract_resume_info_prompt_template,
                )
            )
            | claude_sonnet()
            | parser
        )

        # TODO: error handling here
        resume_info: ResumeInfo = extract_resume_info_chain.invoke(
            {"resume_text": message}
        )

        # Save resume info to session
        # TODO: decouple state and TinyDBSessionService
        self.session_service.update_resume_info(
            session_id=self.session.session_id, resume_info=resume_info
        )

        return ResumeValidationStrategy
