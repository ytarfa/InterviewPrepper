from typing import Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.interview.command.respond_with_messages_command import (
    RespondWithMessagesCommand,
)
from src.core.interview.command.update_session_resume_info_command import (
    UpdateSessionResumeInfoCommand,
)
from src.core.interview.command.update_session_state_command import (
    UpdateSessionStateCommand,
)
from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.prompts.interview.extract_resume_info import (
    extract_resume_info_prompt_template,
)
from src.core.prompts.interview.introduction import get_resume_message
from src.domain.models.message import Message, MessageType
from src.domain.models.resume_info import ResumeInfo
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_sonnet


class ResumeStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session, session_service, interview_message_context):
        super().__init__(
            session=session,
            session_service=session_service,
            interview_message_context=interview_message_context,
        )

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(content=get_resume_message, type=MessageType.SYSTEM)

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.RESUME

    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
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
        resume_info_message = Message(
            content=resume_info.model_dump_json(),
            type=MessageType.SYSTEM,
        )

        return [
            UpdateSessionResumeInfoCommand(
                session_service=self.session_service,
                session_id=self.session.session_id,
                resume_info=resume_info,
            ),
            UpdateSessionStateCommand(
                session_service=self.session_service,
                session_id=self.session.session_id,
                target_state=SessionState.JOB_DESCRIPTION,
            ),
            RespondWithMessagesCommand(
                message=Message(
                    content="This is the information I was able to extract from the resume:",
                    type=MessageType.SYSTEM,
                ),
                interview_message_context=self.interview_message_context,
            ),
            RespondWithMessagesCommand(
                message=resume_info_message,
                interview_message_context=self.interview_message_context,
            ),
        ]
