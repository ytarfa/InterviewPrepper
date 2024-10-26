from abc import ABC, abstractmethod


class InterviewCommand(ABC):
    @abstractmethod
    def execute(self):
        pass
