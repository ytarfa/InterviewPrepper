from typing import Optional, Tuple

from dependency_injector.providers import Callable
from langchain.output_parsers import EnumOutputParser
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
from src.core.messages.ask_for_job_description import ask_for_job_description_message
from src.core.messages.ask_for_resume import ask_for_resume_message
from src.core.messages.start import start_retry_message
from src.core.prompts.interview.intent_classifiers import (
    start_message_intent_classifier_prompt,
    StartMessageIntentClassifierPromptOutput,
)
from src.domain.models.message import Message, MessageType
from src.domain.models.session import SessionState, Session
from src.infrastructure.llm import claude_haiku

RETRY_MESSAGE = Message(content=start_retry_message, type=MessageType.SYSTEM)

TARGET_STATE_MAP: dict[
    StartMessageIntentClassifierPromptOutput, Tuple[SessionState, str]
] = {
    StartMessageIntentClassifierPromptOutput.RESUME: (
        SessionState.RESUME,
        ask_for_resume_message,
    ),
    StartMessageIntentClassifierPromptOutput.JOB_DESCRIPTION: (
        SessionState.JOB_DESCRIPTION,
        ask_for_job_description_message,
    ),
    StartMessageIntentClassifierPromptOutput.OTHER: (None, None),
}


class StartStrategy(InterviewManagerStrategyInterface):
    def __init__(
        self,
        session_id: str,
        command_providers: dict[
            type[InterviewCommand], Callable[..., InterviewCommand]
        ],
    ):
        self.session_id = session_id
        self.command_providers = command_providers

    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
        parser = EnumOutputParser(enum=StartMessageIntentClassifierPromptOutput)
        format_instructions = parser.get_format_instructions()

        chain = (
            PromptTemplate(
                partial_variables={"format_instructions": format_instructions},
                template=start_message_intent_classifier_prompt,
            )
            | claude_haiku()
            | parser
        )

        response = chain.invoke({"message": message})
        (target_state, message_content) = TARGET_STATE_MAP[
            StartMessageIntentClassifierPromptOutput(response)
        ]

        # If intent could not be classified, ask the user for intent again
        if target_state is None:
            return [
                self.command_providers.get(type[RespondWithMessagesCommand])(
                    message=RETRY_MESSAGE
                )
            ]

        response_message = Message(content=message_content, type=MessageType.SYSTEM)
        return [
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=response_message
            ),
            self.command_providers.get(type[UpdateSessionStateCommand])(
                session_id=self.session_id, target_state=target_state
            ),
        ]
