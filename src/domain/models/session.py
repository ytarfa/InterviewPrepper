from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from .interview_question import InterviewQuestion
from .job_description_info import JobDescriptionInfo
from .message import Message, MessageType
from .resume_info import ResumeInfo
from ...core.messages.start import start_message


class SessionState(str, Enum):
    START = "start"
    RESUME = "resume"
    RESUME_VALIDATION = "resume_validation"
    JOB_DESCRIPTION = "job_description"
    JOB_DESCRIPTION_VALIDATION = "job_description_validation"
    INTERVIEW = "interview"
    EVALUATION = "evaluation"


class SessionContext(BaseModel):
    current_interview_question: Optional[InterviewQuestion] = None


class Session(BaseModel):
    session_id: str
    resume_info: Optional[ResumeInfo] = None
    job_description_info: Optional[JobDescriptionInfo] = None
    context: SessionContext = SessionContext()
    # TODO: Move the init message to a strategy?
    messages: list[Message] = [Message(content=start_message, type=MessageType.SYSTEM)]
    state: SessionState = SessionState.START
