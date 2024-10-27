from typing import Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.interview.command.respond_with_messages_command import (
    RespondWithMessagesCommand,
)
from src.core.interview.command.update_session_job_description_command import (
    UpdateSessionJobDescriptionInfoCommand,
)
from src.core.interview.command.update_session_state_command import (
    UpdateSessionStateCommand,
)
from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.prompts.interview.extract_job_description_info import (
    extract_job_description_info_prompt_template,
)
from src.domain.models.job_description_info import JobDescriptionInfo
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_sonnet


class JobDescriptionStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session, session_service, interview_message_context):
        super().__init__(
            session=session,
            session_service=session_service,
            interview_message_context=interview_message_context,
        )

    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
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
        job_description_info_message = Message(
            content=job_description_info.model_dump_json(), type=MessageType.SYSTEM
        )

        return [
            UpdateSessionJobDescriptionInfoCommand(
                session_service=self.session_service,
                session_id=self.session.session_id,
                job_description_info=job_description_info,
            ),
            UpdateSessionStateCommand(
                session_service=self.session_service,
                session_id=self.session.session_id,
                target_state=SessionState.INTERVIEW,
            ),
            RespondWithMessagesCommand(
                message=Message(
                    content="This is the information I was able to extract from the job description:",
                    type=MessageType.SYSTEM,
                ),
                interview_message_context=self.interview_message_context,
            ),
            RespondWithMessagesCommand(
                message=job_description_info_message,
                interview_message_context=self.interview_message_context,
            ),
        ]
