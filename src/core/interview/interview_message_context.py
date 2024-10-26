from src.domain.models.message import Message


class InterviewMessageContext:
    def __init__(self):
        self.messages: list[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages
