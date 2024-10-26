from pydantic import BaseModel, Field


class Education(BaseModel):
    start_date: str = Field(description="Start date of education experience")
    end_date: str = Field(description="End date of education experience")
    degree: str = Field(description="Degree of education experience")
    description: str = Field(description="Description of education experience")


class WorkExperience(BaseModel):
    start_date: str = Field(description="Start date of work experience")
    end_date: str = Field(description="End date of work experience")
    company: str = Field(description="Company of work experience")
    description: str = Field(description="Description of work experience")


class ResumeInfo(BaseModel):
    years_of_experience: int = Field(description="Total years of professional experience as a number"),
    skills: list[str] = Field(description="List of professional skills and technologies"),
    work_experience: list[WorkExperience] = Field(description="List of work experiences, each containing start_date, end_date, company, and description")
    education: list[Education] = Field(description="List of educational experiences, each containing start_date, end_date, degree, and description")