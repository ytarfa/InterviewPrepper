from dependency_injector import containers, providers
from dependency_injector.containers import WiringConfiguration

from src.core.interview.command.command_base import InterviewCommand
from src.core.interview.command.respond_with_messages_command import (
    RespondWithMessagesCommand,
)
from src.core.interview.command.update_session_context_interview_question_command import (
    UpdateSessionContextInterviewQuestionCommand,
)
from src.core.interview.command.update_session_job_description_command import (
    UpdateSessionJobDescriptionInfoCommand,
)
from src.core.interview.command.update_session_resume_info_command import (
    UpdateSessionResumeInfoCommand,
)
from src.core.interview.command.update_session_state_command import (
    UpdateSessionStateCommand,
)
from src.core.interview.interview_manager import InterviewManager
from src.core.interview.interview_message_context import InterviewMessageContext
from src.core.interview.strategy.answer_evaluation_strategy import (
    AnswerEvaluationStrategy,
)
from src.core.interview.strategy.interview_question_strategy import (
    InterviewQuestionStrategy,
)
from src.core.interview.strategy.job_description_strategy import JobDescriptionStrategy
from src.core.interview.strategy.resume_strategy import ResumeStrategy
from src.core.interview.strategy.start_strategy import StartStrategy
from src.core.interview.strategy.strategy_base import InterviewManagerStrategyInterface
from src.core.session.tiny_db_session_service import TinyDBSessionService
from src.domain.models.session import SessionState


class StrategyProvider(providers.Factory):
    provided_type = InterviewManagerStrategyInterface


class CommandProvider(providers.Factory):
    provided_type = InterviewCommand


class Container(containers.DeclarativeContainer):

    wiring_config = WiringConfiguration(modules=[".api.sessions_routes"])

    session_service = providers.Singleton(TinyDBSessionService)

    interview_message_context = providers.Singleton(InterviewMessageContext)

    # Commands providers
    respond_with_messages_command = CommandProvider(
        RespondWithMessagesCommand, interview_message_context=interview_message_context
    )
    update_session_state_command = CommandProvider(
        UpdateSessionStateCommand, session_service=session_service
    )
    update_session_resume_info_command = CommandProvider(
        UpdateSessionResumeInfoCommand, session_service=session_service
    )
    update_session_job_description_info_command = CommandProvider(
        UpdateSessionJobDescriptionInfoCommand, session_service=session_service
    )
    update_session_context_interview_question_command = CommandProvider(
        UpdateSessionContextInterviewQuestionCommand, session_service=session_service
    )

    command_providers = providers.Dict(
        {
            type[RespondWithMessagesCommand]: respond_with_messages_command.provider,
            type[UpdateSessionStateCommand]: update_session_state_command.provider,
            type[
                UpdateSessionResumeInfoCommand
            ]: update_session_resume_info_command.provider,
            type[
                UpdateSessionJobDescriptionInfoCommand
            ]: update_session_job_description_info_command.provider,
            type[
                UpdateSessionContextInterviewQuestionCommand
            ]: update_session_context_interview_question_command.provider,
        }
    )

    # Strategy providers
    start_strategy = StrategyProvider(
        StartStrategy, command_providers=command_providers
    )
    interview_question_strategy = StrategyProvider(
        InterviewQuestionStrategy,
        command_providers=command_providers,
        session_service=session_service,
    )
    answer_evaluation_strategy = StrategyProvider(
        AnswerEvaluationStrategy,
        command_providers=command_providers,
        session_service=session_service,
    )
    resume_strategy = StrategyProvider(
        ResumeStrategy,
        command_providers=command_providers,
        session_service=session_service,
        interview_question_strategy_provider=interview_question_strategy.provider,
    )
    job_description_strategy = StrategyProvider(
        JobDescriptionStrategy,
        command_providers=command_providers,
        session_service=session_service,
        interview_question_strategy_provider=interview_question_strategy.provider,
    )

    strategy_providers = providers.Dict(
        {
            SessionState.START: start_strategy.provider,
            SessionState.RESUME: resume_strategy.provider,
            SessionState.JOB_DESCRIPTION: job_description_strategy.provider,
            SessionState.INTERVIEW: interview_question_strategy.provider,
            SessionState.EVALUATION: answer_evaluation_strategy.provider,
        }
    )

    interview_manager = providers.Factory(
        InterviewManager,
        session_service=session_service,
        strategy_providers=strategy_providers,
    )
