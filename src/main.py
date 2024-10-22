from fastapi import FastAPI
from pydantic import BaseModel
from .api.inverview_service import InterviewService
from .api.session_service import TinyDBSessionService

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


@app.get("/api/sessions")
async def get_all_sessions():
    session_service = TinyDBSessionService()
    return session_service.get_all_sessions()


@app.post("/api/sessions")
async def create_session():
    session_service = TinyDBSessionService()
    return session_service.create_session()


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    session_service = TinyDBSessionService()
    return session_service.get_session(session_id)


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
