from dataclasses import dataclass

from .message import Message


@dataclass
class Session:
    session_id: str
    resume: str = None
    job_description: str = None
    resume_skills: list = None
    job_description_skills: list = None
    yoe: int = None
    messages: list[Message] = None
