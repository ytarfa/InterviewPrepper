from abc import ABC
from typing import Optional

from ...domain.models.session import Session


class InterviewManagerState(ABC):
    def __init__(self, session: Session):
        self.session = session

    async def handle_message(self, message: Optional[str]):
        pass
