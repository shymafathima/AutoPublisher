from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator

from schemas.common_schema import Source, Evidence

class ResearcherOutput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    topic: str = Field(min_length=1)
    research_summary: str = Field(min_length=1)

    sources: List[Source] = Field(default_factory=list)
    key_findings: List[str] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    research_gaps: List[str] = Field(default_factory=list)
    @model_validator(mode="after")
    def validate_research_references(self):
        source_ids = [source.source_id for source in self.sources]
        evidence_ids = [item.evidence_id for item in self.evidence]

        if len(source_ids) != len(set(source_ids)):
            raise ValueError("Duplicate source IDs found")

        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("Duplicate evidence IDs found")

        valid_source_ids = set(source_ids)

        source_url_map = {
            source.source_id: str(source.url)
            for source in self.sources
        }

        for item in self.evidence:
            if item.source_id not in valid_source_ids:
                raise ValueError(
                    f"Evidence {item.evidence_id} refers to unknown source ID: {item.source_id}"
                )

            if str(item.supporting_url) != source_url_map[item.source_id]:
                raise ValueError(
                    f"Evidence {item.evidence_id} has a URL that does not match its source"
                )

        return self
        