extract_resume_info_prompt_template = """
    You are a professional resume parser. Extract the following information from the provided resume text in a structured format.
    Follow these guidelines:
    - For years of experience: Calculate the total professional experience based on work history
    - For skills: Extract all technical and professional skills mentioned
    - For work experience: Include all positions with their full details
    - For education: Include all degrees and certifications with their full details
    - Dates should be in YYYY-MM format
    - If end date is current/present, use "present"
    - If any field is missing, use null
    
    Resume text:
    {resume_text}
    
    {format_instructions}
"""
