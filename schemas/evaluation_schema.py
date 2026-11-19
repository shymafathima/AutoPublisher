from typing import List, Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)

def calculate_weighted_score(
    accuracy,
    clarity,
    structure,
    tone,
    originality,
    engagement
):
    score = (
        (accuracy / 5 * 30)
        + (clarity / 5 * 20)
        + (structure / 5 * 15)
        + (tone / 5 * 15)
        + (originality / 5 * 10)
        + (engagement / 5 * 10)
    )

    return round(score, 2)

class ContentEvaluation(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    accuracy: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    structure: int = Field(ge=1, le=5)
    tone: int = Field(ge=1, le=5)
    originality: int = Field(ge=1, le=5)
    engagement: int = Field(ge=1, le=5)

    overall_score: float = Field(default=0, ge=0, le=100)

    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    revision_suggestions: List[str] = Field(default_factory=list)

    evaluation_status: Literal[
        "Accepted",
        "Revision Required",
        "Human Review"
    ]
    @model_validator(mode="after")
    def calculate_overall_score(self):
        self.overall_score = calculate_weighted_score(
            accuracy=self.accuracy,
            clarity=self.clarity,
            structure=self.structure,
            tone=self.tone,
            originality=self.originality,
            engagement=self.engagement
        )

        return self
    @field_validator(
        "strengths",
        "weaknesses",
        "revision_suggestions",
        mode="before"
    )
    @classmethod
    def validate_feedback_items(cls, value):
        if value is None:
            return value

        if any(not item.strip() for item in value):
            raise ValueError("Feedback items cannot be empty")

        return value