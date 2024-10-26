extract_job_description_info_prompt_template = """
    You are a professional job description analyzer. Extract and structure the following information from the provided job posting text.

    Follow these guidelines:

    Basic Information:
    - Extract the job title, department, and company name
    - Determine the seniority level (entry, mid, senior, lead, manager)
    - Create a concise summary of the position

    Responsibilities:
    - List all job responsibilities
    - Categorize each responsibility (development, management, communication, etc.)
    - Maintain the original meaning while standardizing the format

    Requirements:
    - Extract all requirements and preferences
    - Categorize each requirement (technical, soft_skill, education, certification)
    - Mark each requirement as required (true) or preferred (false)
    - Include years of experience requirements where specified

    Important Notes:
    - Use null for any missing fields
    - Maintain original intent and requirements
    - Don't infer information that isn't explicitly stated
    - Categories should be lowercase and snake_case

    Job Description Text:
    {job_description_text}

    {format_instructions}
"""
