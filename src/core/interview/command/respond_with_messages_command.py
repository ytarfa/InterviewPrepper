from src.core.interview.command.command_base import (
    InterviewCommand,
)
from src.core.interview.interview_message_context import InterviewMessageContext
from src.domain.models.message import Message


class RespondWithMessagesCommand(InterviewCommand):
    def __init__(
        self, message: Message, interview_message_context: InterviewMessageContext
    ):
        self.message = message
        self.interview_message_context = interview_message_context

    def execute(self):
        self.interview_message_context.add_message(self.message)
