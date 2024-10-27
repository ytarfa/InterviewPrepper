from typing import Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.interview.command.respond_with_messages_command import (
    RespondWithMessagesCommand,
)
from src.core.interview.command.update_session_state_command import (
    UpdateSessionStateCommand,
)
from src.core.interview.strategy.strategy_base import (
    InterviewManagerStrategyInterface,
)
from src.core.interview.strategy.job_description_strategy import (
    JobDescriptionStrategy,
)
from src.core.interview.strategy.resume_strategy import (
    ResumeStrategy,
)
from src.core.prompts.interview.introduction import (
    start_message_intent_classifier_prompt,
    StartMessageClassifierPromptOutput,
)
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_haiku


target_state_map: dict[StartMessageClassifierPromptOutput, SessionState] = {
    StartMessageClassifierPromptOutput.RESUME: SessionState.RESUME,
    StartMessageClassifierPromptOutput.JOB_DESCRIPTION: SessionState.JOB_DESCRIPTION,
    # TODO: Create state for 'other'
    StartMessageClassifierPromptOutput.OTHER: SessionState.RESUME,
}


class StartStrategy(InterviewManagerStrategyInterface):
    def __init__(self, session, session_service, interview_message_context):
        super().__init__(
            session=session,
            session_service=session_service,
            interview_message_context=interview_message_context,
        )

    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
        chain = (
            PromptTemplate.from_template(start_message_intent_classifier_prompt)
            | claude_haiku()
            | StrOutputParser()
        )
        response = chain.invoke({"message": message})
        response_message = Message(content=response, type=MessageType.SYSTEM)
        # TODO: response should be casted to the enum and validated
        return [
            RespondWithMessagesCommand(
                message=response_message,
                interview_message_context=self.interview_message_context,
            ),
            UpdateSessionStateCommand(
                session_id=self.session.session_id,
                session_service=self.session_service,
                target_state=target_state_map[
                    StartMessageClassifierPromptOutput(response)
                ],
            ),
        ]
