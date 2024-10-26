from pydantic import BaseModel, Field
from typing import List, Optional


class Requirement(BaseModel):
    category: str = Field(
        description="Category of requirement (e.g., 'technical', 'soft_skill', 'education', 'certification')"
    )
    description: str = Field(description="Description of the requirement")
    is_required: bool = Field(
        description="Whether this requirement is mandatory or preferred"
    )


class Responsibility(BaseModel):
    category: str = Field(
        description="Category of responsibility (e.g., 'development', 'management', 'communication')"
    )
    description: str = Field(description="Description of the responsibility")


class JobDescriptionInfo(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    seniority_level: str = Field(
        description="Seniority level (e.g., 'entry', 'mid', 'senior', 'lead', 'manager')"
    )
    skills: list[str] = (
        Field(description="List of professional skills and technologies"),
    )

    summary: str = Field(description="Brief summary or overview of the position")
    responsibilities: List[Responsibility] = Field(
        description="List of job responsibilities"
    )
    requirements: List[Requirement] = Field(
        description="List of job requirements including skills, education, and experience"
    )
