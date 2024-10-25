from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    USER = "user"
    SYSTEM = "system"


@dataclass
class Message:
    message: str
    type: str
