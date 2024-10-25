from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    USER = "user"
    SYSTEM = "system"


class Message(BaseModel):
    content: str
    type: MessageType
