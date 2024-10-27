from typing import Optional

from pydantic import BaseModel, Field


class StarFormatEvaluation(BaseModel):
    score: int = Field(
        ge=1, le=5, description="Score from 1-5 for STAR format adherence"
    )
    feedback: str = Field(description="Overall feedback on STAR format usage")
    examples: dict[str, str] = Field(
        description="Examples of how each STAR component was addressed"
    )


class DimensionEvaluation(BaseModel):
    score: int = Field(ge=1, le=5, description="Score from 1-5 for this dimension")
    feedback: str = Field(description="Detailed feedback for this dimension")
    key_points: list[str] = Field(description="Key points noted in the evaluation")


class DetailedEvaluation(BaseModel):
    score: int = Field(ge=1, le=5, description="Score from 1-5 for this dimension")
    feedback: str = Field(description="Detailed feedback for this dimension")
    strengths: list[str] = Field(description="Specific strengths demonstrated")
    areas_for_improvement: list[str] = Field(description="Areas that could be improved")


class OverallEvaluation(BaseModel):
    summary: str = Field(description="2-3 sentence overall assessment")
    recommendation: str = Field(
        description="Hire recommendation (Strong Yes, Yes, Maybe, No, Strong No)"
    )
    key_strengths: list[str] = Field(
        description="Key strengths demonstrated in the answer"
    )
    improvement_areas: list[str] = Field(description="Areas needing improvement")


class FeedbackPoints(BaseModel):
    positive: list[str] = Field(
        description="Specific positive feedback points to share with candidate"
    )
    constructive: list[str] = Field(
        description="Constructive feedback points to share with candidate"
    )


class AnswerEvaluation(BaseModel):
    star_format: Optional[StarFormatEvaluation] = Field(
        description="Evaluation of STAR format usage, if applicable"
    )
    technical_accuracy: DimensionEvaluation = Field(
        description="Evaluation of technical accuracy"
    )
    problem_solving: DimensionEvaluation = Field(
        description="Evaluation of problem-solving approach"
    )
    communication: DetailedEvaluation = Field(
        description="Evaluation of communication quality"
    )
    completeness: DimensionEvaluation = Field(
        description="Evaluation of response completeness"
    )
    relevance: DimensionEvaluation = Field(
        description="Evaluation of relevance and focus"
    )
    overall_evaluation: OverallEvaluation = Field(
        description="Overall evaluation and recommendation"
    )
    feedback_to_candidate: FeedbackPoints = Field(
        description="Structured feedback points to share with the candidate"
    )
