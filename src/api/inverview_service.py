from typing import Dict, Any
from ..models.interview_chain import InterviewManager, InterviewContext


class InterviewService:
    def __init__(self):
        self.interview_manager = InterviewManager()

    def start_interview(self, resume: str, job_description: str) -> Dict[str, Any]:
        context = InterviewContext(
            resume=resume,
            job_description=job_description
        )

        question = self.interview_manager.generate_question(context)
        return {
            "question": question,
            "resume": resume,
            "job_description": job_description
        }

    def handle_answer(
        self,
        resume: str,
        job_description: str,
        current_question: str,
        answer: str,
        generate_followup: bool = False
    ) -> Dict[str, Any]:
        context = InterviewContext(
            resume=resume,
            job_description=job_description,
            current_question=current_question,
            previous_answer=answer if generate_followup else None
        )

        feedback = self.interview_manager.evaluate_answer(context, answer)
        next_question = None

        if generate_followup:
            next_question = self.interview_manager.generate_question(context)

        return {
            "feedback": feedback,
            "next_question": next_question
        }
