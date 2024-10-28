from dependency_injector import containers, providers
from dependency_injector.containers import WiringConfiguration

from src.core.interview.interview_manager import InterviewManager
from src.core.interview.interview_message_context import InterviewMessageContext
from src.core.interview.strategy.strategy_factory import StrategyFactory
from src.core.session.tiny_db_session_service import TinyDBSessionService


class Container(containers.DeclarativeContainer):

    wiring_config = WiringConfiguration(modules=[".api.sessions_routes"])

    session_service = providers.Singleton(TinyDBSessionService)

    interview_message_context = providers.Singleton(InterviewMessageContext)

    strategy_factory = providers.Singleton(
        StrategyFactory,
        session_service=session_service,
        interview_message_context=interview_message_context,
    )

    interview_manager = providers.Factory(
        InterviewManager,
        session_service=session_service,
        strategy_factory=strategy_factory,
    )
