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
from src.core.interview.command.update_session_context_interview_question_command import (
    UpdateSessionContextInterviewQuestionCommand,
)
from src.core.interview.command.update_session_state_command import (
    UpdateSessionStateCommand,
)
from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.prompts.interview.generate_interview_question import (
    generate_interview_question_prompt,
)
from src.core.session.session_service import SessionService
from src.domain.models.interview_question import InterviewQuestion
from src.domain.models.message import Message, MessageType, InterviewQuestionMessage
from src.domain.models.session import SessionState, Session
from src.infrastructure.llm import claude_sonnet


class InterviewQuestionStrategy(InterviewManagerStrategyInterface):
    def __init__(
        self,
        session_id: str,
        session_service: SessionService,
        command_providers: dict[
            type[InterviewCommand], Callable[..., InterviewCommand]
        ],
    ):
        self.session_id = session_id
        self.session_service = session_service
        self.command_providers = command_providers

    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
        parser = PydanticOutputParser(pydantic_object=InterviewQuestion)
        format_instructions = parser.get_format_instructions()
        chain = (
            (
                PromptTemplate(
                    input_variables=["resume", "job_description"],
                    partial_variables={"format_instructions": format_instructions},
                    template=generate_interview_question_prompt,
                )
            )
            | claude_sonnet()
            | parser
        )

        session = self.session_service.get_session(self.session_id)
        interview_question: InterviewQuestion = chain.invoke(
            {
                "resume": session.resume_info,
                "job_description": session.job_description_info,
            }
        )
        interview_question_message = InterviewQuestionMessage(
            content=interview_question.model_dump_json(),
            type=MessageType.SYSTEM,
            interview_question=interview_question,
        )

        return [
            self.command_providers.get(
                type[UpdateSessionContextInterviewQuestionCommand]
            )(session_id=self.session_id, interview_question=interview_question),
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=interview_question_message
            ),
            self.command_providers.get(type[UpdateSessionStateCommand])(
                session_id=self.session_id, target_state=SessionState.EVALUATION
            ),
        ]
