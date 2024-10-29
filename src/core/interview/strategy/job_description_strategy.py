from typing import Optional

from dependency_injector.providers import Callable
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
from src.core.interview.strategy.interview_question_strategy import (
    InterviewQuestionStrategy,
)
from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.messages.ask_for_resume import ask_for_resume_message
from src.core.prompts.interview.extract_job_description_info import (
    extract_job_description_info_prompt_template,
)
from src.core.session.session_service import SessionService
from src.domain.models.job_description_info import JobDescriptionInfo
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState, Session
from src.infrastructure.llm import claude_sonnet


class JobDescriptionStrategy(InterviewManagerStrategyInterface):
    def __init__(
        self,
        session_id: str,
        session_service: SessionService,
        command_providers: dict[
            type[InterviewCommand], Callable[..., InterviewCommand]
        ],
        interview_question_strategy_provider: Callable[..., InterviewQuestionStrategy],
    ):
        self.session_id = session_id
        self.command_providers = command_providers
        self.session_service = session_service
        self.interview_question_strategy_provider = interview_question_strategy_provider

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

        commands = [
            self.command_providers.get(type[UpdateSessionJobDescriptionInfoCommand])(
                session_id=self.session_id, job_description_info=job_description_info
            ),
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=Message(
                    content="This is the information I was able to extract from the job description:",
                    type=MessageType.SYSTEM,
                )
            ),
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=job_description_info_message
            ),
        ]

        session = self.session_service.get_session(self.session_id)
        if session.resume_info is None:
            # If session.resume_info is None ask for resume
            commands.extend(
                [
                    self.command_providers.get(type[UpdateSessionStateCommand])(
                        session_id=self.session_id,
                        target_state=SessionState.RESUME,
                    ),
                    self.command_providers.get(type[RespondWithMessagesCommand])(
                        message=Message(
                            content=ask_for_resume_message,
                            type=MessageType.SYSTEM,
                        )
                    ),
                ]
            )
        else:
            # Else go to interview
            interview_strategy: InterviewQuestionStrategy = (
                self.interview_question_strategy_provider(session_id=self.session_id)
            )
            interview_commands = await interview_strategy.handle_message()
            commands.extend(interview_commands)

        return commands
