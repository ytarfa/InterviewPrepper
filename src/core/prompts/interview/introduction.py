from enum import Enum

start_message = """
    Welcome to Interview Prepper! We'll start by gathering some information we need to proceed with the mock interview.
    To start, choose whether you'd like to provide your resume or a job description?
"""

start_message_intent_classifier_prompt = """
    Given the user message below, classify the user's intent as either being 'resume', 'job_description' or 'other'.
    Do not respond with more than one word. Do not respond with anything other than 'resume', 'job_description' or 'other'
    
    <message>
    {message}
    <message>
    
    Classification:
"""


class StartMessageClassifierPromptOutput(Enum):
    RESUME = "resume"
    JOB_DESCRIPTION = "job_description"
    OTHER = "other"


get_resume_message = """
    Please paste your resume in the chat.
"""

get_job_description_message = """
    Please paste the job description in the chat.
"""
