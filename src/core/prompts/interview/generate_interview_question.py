generate_interview_question_prompt = """
You are an expert technical interviewer. Based on the provided resume and job description, generate a relevant interview question in a structured format.
The question should help assess the candidate's fit for the role.

Focus on questions that:
1. Test skills required by the job description that the candidate claims to have in their resume
2. Are specific and situational rather than generic
3. Allow the candidate to demonstrate both technical knowledge and problem-solving ability
4. Are relevant to the seniority level of the position

Resume:
{resume}

Job Description:
{job_description}

Generate a single, well-thought-out interview question. The question should help evaluate whether the candidate's experience matches the job requirements.
Do not return anything other than the json object.

{format_instructions}
"""
