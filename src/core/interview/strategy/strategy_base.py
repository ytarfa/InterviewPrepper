import abc
from abc import ABC
from typing import Optional

from src.core.interview.command.command_base import (
    InterviewCommand,
)


class InterviewManagerStrategyInterface(ABC):

    @abc.abstractmethod
    async def handle_message(self, message: Optional[str]) -> list[InterviewCommand]:
        pass
