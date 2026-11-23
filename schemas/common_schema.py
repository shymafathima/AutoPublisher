
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class TopicInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    topic: str = Field(min_length=1)
    target_audience: str = Field(min_length=1)
    content_type: str
    tone: str = Field(min_length=1)
    keywords: List[str]
    content_goal: Optional[str] = None

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, value):
        allowed = ["blog", "linkedin", "newsletter"]

        if value.lower() not in allowed:
            raise ValueError("Invalid content type")

        return value.lower()


class Source(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: HttpUrl
    publisher: str = Field(min_length=1)
    published_date: Optional[datetime] = None
    retrieved_at: datetime
    relevance_score: float = Field(ge=0, le=1)


class Evidence(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    evidence_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    claim_or_finding: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    supporting_url: HttpUrl
