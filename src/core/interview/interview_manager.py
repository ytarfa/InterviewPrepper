from ..session.session_service import SessionService

from abc import ABC


class InterviewManagerState(ABC):
    def __init__(self, session_service: SessionService, session_id: str):
        self.session_service = session_service
        self.session = self.session_service.get_session(session_id)

    def handle_message(self):
        pass


class InterviewManager:
    def __init__(self, state: InterviewManagerState):
        self.state = state

    def handle_message(self):
        self.state.handle_message()
