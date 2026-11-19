from typing import List
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    field_validator
)
from schemas.research_schema import ResearcherOutput

class OutlinerInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    topic: str = Field(min_length=1)
    research: ResearcherOutput

class OutlineSection(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    heading: str = Field(min_length=1)
    key_points: List[str]
    evidence_ids: List[str]

    @field_validator("key_points")
    @classmethod
    def validate_key_points(cls, value):
        if any(not point for point in value):
            raise ValueError("Key points cannot be empty")

        return value

    @field_validator("evidence_ids")
    @classmethod
    def validate_evidence_ids(cls, value):
        if any(not evidence_id for evidence_id in value):
            raise ValueError("Evidence IDs cannot be empty")

        return value

class OutlinerOutput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1)
    introduction: str = Field(min_length=1)
    sections: List[OutlineSection] = Field(min_length=1)
    conclusion: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_headings(self):
        headings = [section.heading.lower() for section in self.sections]

        if len(headings) != len(set(headings)):
            raise ValueError("Duplicate section headings found")

        return self
def validate_outline_evidence(
    outline: OutlinerOutput,
    research: ResearcherOutput
):
    valid_evidence_ids = {
        item.evidence_id for item in research.evidence
    }

    for section in outline.sections:
        for evidence_id in section.evidence_ids:
            if evidence_id not in valid_evidence_ids:
                raise ValueError(
                    f"Outline uses unknown evidence ID: {evidence_id}"
                )

    return outline
