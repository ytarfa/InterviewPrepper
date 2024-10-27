from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel

from src.domain.models.answer_evaluation import AnswerEvaluation
from src.domain.models.interview_question import InterviewQuestion


class MessageType(str, Enum):
    USER = "user"
    SYSTEM = "system"


class Message(BaseModel):
    content: str
    type: MessageType


class InterviewQuestionMessage(Message):
    interview_question: InterviewQuestion


class AnswerEvaluationMessage(Message):
    evaluation: AnswerEvaluation
