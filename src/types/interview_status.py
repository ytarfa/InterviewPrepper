from dataclasses import dataclass
from enum import Enum


class InterviewStage(Enum):
    RESUME = "resume"
    JOB_DESCRIPTION = "job_description"
    QUESTION = "question"
    ANSWER = "answer"
    EVALUATION = "evaluation"


@dataclass
class InterviewStatus:
    stage: InterviewStage
