from dataclasses import dataclass
from typing import Optional
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

@dataclass
class InterviewContext:
    resume: str
    job_description: str
    current_question: Optional[str] = None
    previous_answer: Optional[str] = None

class InterviewChainFactory:
    @staticmethod
    def create_prompt_templates():
        question_template = """
        Based on this resume:
        {resume}

        And this job description:
        {job_description}

        Act as an interviewer and generate ONE relevant technical or behavioral interview question.
        The question should be specific to the candidate's background and the job requirements.
        Only return the question itself, nothing else.
        """

        followup_template = """
        Based on this resume:
        {resume}

        And this job description:
        {job_description}

        Previous question: {previous_question}
        Candidate's answer: {previous_answer}

        Generate ONE follow-up question that dives deeper into the topic or explores a related aspect.
        The follow-up should help evaluate the candidate's depth of knowledge or experience.
        Only return the question itself, nothing else.
        """

        evaluation_template = """
        Context:
        - Resume: {resume}
        - Job Description: {job_description}
        - Interview Question: {question}
        - Candidate's Answer: {answer}

        Evaluate the candidate's answer. Consider:
        1. Relevance to the question
        2. Technical accuracy (if applicable)
        3. Communication clarity
        4. Specific examples provided

        Provide constructive feedback including:
        - What was done well
        - Areas for improvement
        - Specific suggestions for a better answer

        Keep the feedback professional and encouraging.
        """

        return {
            "question": ChatPromptTemplate.from_template(question_template),
            "followup": ChatPromptTemplate.from_template(followup_template),
            "evaluation": ChatPromptTemplate.from_template(evaluation_template)
        }

    @staticmethod
    def create_chains():
        llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
        templates = InterviewChainFactory.create_prompt_templates()

        return {
            "question": LLMChain(llm=llm, prompt=templates["question"]),
            "followup": LLMChain(llm=llm, prompt=templates["followup"]),
            "evaluation": LLMChain(llm=llm, prompt=templates["evaluation"])
        }


class InterviewManager:
    def __init__(self):
        self.chains = InterviewChainFactory.create_chains()

    def generate_question(self, context: InterviewContext) -> str:
        if context.current_question is None or context.previous_answer is None:
            return self.chains["question"].run(
                resume=context.resume,
                job_description=context.job_description
            )
        else:
            return self.chains["followup"].run(
                resume=context.resume,
                job_description=context.job_description,
                previous_question=context.current_question,
                previous_answer=context.previous_answer
            )

    def evaluate_answer(self, context: InterviewContext, answer: str) -> str:
        return self.chains["evaluation"].run(
            resume=context.resume,
            job_description=context.job_description,
            question=context.current_question,
            answer=answer
        )