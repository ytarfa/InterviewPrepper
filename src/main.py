from fastapi import FastAPI
from pydantic import BaseModel
from .api.inverview_service import InterviewService


app = FastAPI()
interview_service = InterviewService()


class InterviewStart(BaseModel):
    resume: str
    job_description: str


class AnswerSubmission(BaseModel):
    resume: str
    job_description: str
    current_question: str
    answer: str
    generate_followup: bool = False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/interview/start")
async def start_interview(data: InterviewStart):
    return interview_service.start_interview(
        data.resume,
        data.job_description
    )


@app.post("/api/interview/answer")
async def handle_answer(data: AnswerSubmission):
    return interview_service.handle_answer(
        data.resume,
        data.job_description,
        data.current_question,
        data.answer,
        data.generate_followup
    )
