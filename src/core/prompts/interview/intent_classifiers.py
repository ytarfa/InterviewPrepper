from enum import Enum

start_message_intent_classifier_prompt = """
    Given the user message below, classify the user's intent as either being 'resume', 'job_description'.
    If you are not able to classify the user's intent, respond with 'other'.
    Do not respond with more than one word. Do not respond with anything other than 'resume', 'job_description' or 'other'
    
    <message>
    {message}
    <message>
    
    Classification:
    
    {format_instructions}
"""


class StartMessageIntentClassifierPromptOutput(Enum):
    RESUME = "resume"
    JOB_DESCRIPTION = "job_description"
    OTHER = "other"
