from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question to be asked")
    expected_skills: list[str] = Field(
        description="Skills or knowledge being tested by this question"
    )
