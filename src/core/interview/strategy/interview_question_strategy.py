from typing import Optional

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
from src.domain.models.interview_question import InterviewQuestion
from src.domain.models.message import Message, MessageType, InterviewQuestionMessage
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_sonnet


class InterviewQuestionStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session, session_service, interview_message_context):
        super().__init__(
            session=session,
            session_service=session_service,
            interview_message_context=interview_message_context,
        )

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

        interview_question: InterviewQuestion = chain.invoke(
            {
                "resume": self.session.resume_info,
                "job_description": self.session.job_description_info,
            }
        )
        interview_question_message = InterviewQuestionMessage(
            content=interview_question.model_dump_json(),
            type=MessageType.SYSTEM,
            interview_question=interview_question,
        )

        return [
            UpdateSessionContextInterviewQuestionCommand(
                session_id=self.session.session_id,
                session_service=self.session_service,
                interview_question=interview_question,
            ),
            RespondWithMessagesCommand(
                message=interview_question_message,
                interview_message_context=self.interview_message_context,
            ),
            UpdateSessionStateCommand(
                session_id=self.session.session_id,
                session_service=self.session_service,
                target_state=SessionState.EVALUATION,
            ),
        ]
