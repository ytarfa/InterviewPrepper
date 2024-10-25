from typing import Optional

from .interview_manager_state import InterviewManagerState


class InterviewManagerStartState(InterviewManagerState):
    def __init__(self, session):
        super().__init__(session)

    async def handle_message(self, message: Optional[str]):
        return "Welcome to the interview manager. Type 'start' to begin a new interview session."
