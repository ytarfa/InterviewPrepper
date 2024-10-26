from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .job_description_info import JobDescriptionInfo
from .message import Message, MessageType
from .resume_info import ResumeInfo
from ...core.prompts.interview.introduction import start_message


class SessionState(str, Enum):
    START = "start"
    RESUME = "resume"
    RESUME_VALIDATION = "resume_validation"
    JOB_DESCRIPTION = "job_description"
    JOB_DESCRIPTION_VALIDATION = "job_description_validation"
    INTERVIEW = "interview"


class Session(BaseModel):
    session_id: str
    resume_info: Optional[ResumeInfo] = None
    job_description_info: Optional[JobDescriptionInfo] = None
    messages: list[Message] = [Message(content=start_message, type=MessageType.SYSTEM)]
    state: SessionState = SessionState.START
