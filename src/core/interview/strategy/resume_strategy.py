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
from src.core.interview.command.update_session_resume_info_command import (
    UpdateSessionResumeInfoCommand,
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
from src.core.messages.ask_for_job_description import ask_for_job_description_message
from src.core.prompts.interview.extract_resume_info import (
    extract_resume_info_prompt_template,
)
from src.core.session.session_service import SessionService
from src.domain.models.message import Message, MessageType
from src.domain.models.resume_info import ResumeInfo
from src.domain.models.session import SessionState, Session
from src.infrastructure.llm import claude_sonnet


class ResumeStrategy(InterviewManagerStrategyInterface):
    def __init__(
        self,
        session_id: str,
        session_service: SessionService,
        command_providers: dict[
            type[InterviewCommand], Callable[..., InterviewCommand]
        ],
        interview_question_strategy_provider: Callable[..., InterviewQuestionStrategy],
    ):
        self.session_service = session_service
        self.session_id = session_id
        self.command_providers = command_providers
        self.interview_question_strategy_provider = interview_question_strategy_provider

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

        commands = [
            self.command_providers.get(type[UpdateSessionResumeInfoCommand])(
                session_id=self.session_id, resume_info=resume_info
            ),
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=Message(
                    content="This is the information I was able to extract from the resume:",
                    type=MessageType.SYSTEM,
                )
            ),
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=resume_info_message
            ),
        ]

        session = self.session_service.get_session(self.session_id)
        if session.job_description_info is None:
            # If session.job_description_info is None ask for job description
            commands.extend(
                [
                    self.command_providers.get(type[UpdateSessionStateCommand])(
                        session_id=self.session_id,
                        target_state=SessionState.JOB_DESCRIPTION,
                    ),
                    self.command_providers.get(type[RespondWithMessagesCommand])(
                        message=Message(
                            content=ask_for_job_description_message,
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
