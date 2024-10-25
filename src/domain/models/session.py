from dataclasses import dataclass
from enum import Enum

from .message import Message


class SessionStage(str, Enum):
    START = "start"


@dataclass
class Session:
    session_id: str
    resume: str = None
    job_description: str = None
    resume_skills: list = None
    job_description_skills: list = None
    yoe: int = None
    messages: list[Message] = None
    stage: SessionStage = SessionStage.START
