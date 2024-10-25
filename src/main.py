from fastapi import FastAPI
from pydantic import BaseModel
from .core.session.session_service import TinyDBSessionService


app = FastAPI()


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


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    session_service = TinyDBSessionService()
    return session_service.delete_session(session_id)


@app.delete("/api/sessions")
async def delete_all_sessions():
    session_service = TinyDBSessionService()
    return session_service.delete_all_sessions()
