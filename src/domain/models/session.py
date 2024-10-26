from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .message import Message


class SessionState(str, Enum):
    START = "start"
    RESUME = "resume"
    RESUME_VALIDATION = "resume_validation"
    JOB_DESCRIPTION = "job_description"
    JOB_DESCRIPTION_VALIDATION = "job_description_validation"


class Session(BaseModel):
    session_id: str
    resume: Optional[str] = None
    job_description: Optional[str] = None
    resume_skills: Optional[list] = None
    job_description_skills: Optional[list] = None
    yoe: Optional[int] = None
    messages: Optional[list[Message]] = None
    state: SessionState = SessionState.START
