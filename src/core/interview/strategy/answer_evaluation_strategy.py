from typing import Optional

from dependency_injector.providers import Callable
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.command.command_base import InterviewCommand
from src.core.interview.command.respond_with_messages_command import (
    RespondWithMessagesCommand,
)
from src.core.interview.strategy.strategy_base import InterviewManagerStrategyInterface
from src.core.prompts.interview.evaluate_answer import evaluate_answer_prompt
from src.core.session.session_service import SessionService
from src.domain.models.answer_evaluation import AnswerEvaluation
from src.domain.models.message import (
    MessageType,
    AnswerEvaluationMessage,
)
from src.infrastructure.llm import claude_sonnet


class AnswerEvaluationStrategy(InterviewManagerStrategyInterface):
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
        parser = PydanticOutputParser(pydantic_object=AnswerEvaluation)
        format_instructions = parser.get_format_instructions()
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=claude_sonnet())

        chain = (
            (
                PromptTemplate(
                    input_variables=[
                        "interview_question",
                        "expected_skills",
                        "candidate_answer",
                    ],
                    partial_variables={"format_instructions": format_instructions},
                    template=evaluate_answer_prompt,
                )
            )
            | claude_sonnet()
            | fixing_parser
        )
        session = self.session_service.get_session(session_id=self.session_id)
        interview_question = session.context.current_interview_question
        evaluation = chain.invoke(
            {
                "interview_question": interview_question.question,
                "expected_skills": interview_question.expected_skills,
                "candidate_answer": message,
            }
        )

        evaluation_message = AnswerEvaluationMessage(
            content=evaluation.model_dump_json(),
            type=MessageType.SYSTEM,
            evaluation=evaluation,
        )

        return [
            self.command_providers.get(type[RespondWithMessagesCommand])(
                message=evaluation_message
            )
        ]
