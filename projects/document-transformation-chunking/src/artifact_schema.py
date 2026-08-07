from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, ValidationError, model_validator

ARTIFACT_TYPES = {
    "semantic_chunk",
    "contextual_chunk",
    "summary",
    "raptor",
    "qa_pairs",
    "factoids",
}

REQUIRED_EXTENSION_FIELDS: dict[str, set[str]] = {
    "semantic_chunk": {"token_count", "start_offset", "end_offset"},
    "contextual_chunk": {"token_count", "start_offset", "end_offset", "header", "neighbor_context"},
    "summary": {"summary_text", "summary_length"},
    "raptor": {"node_id", "parent_node_id", "level"},
    "qa_pairs": {"question", "answer", "confidence"},
    "factoids": {"fact", "canonical_value", "confidence"},
}


class DocumentMetadata(BaseModel):
    document_id: str
    source_uri: str
    source_type: str
    title: str | None = None


class LineageMetadata(BaseModel):
    parent_artifact_id: str | None = None
    source_ref: str
    page_number: int | None = None
    section_ref: str | None = None


class ProcessingMetadata(BaseModel):
    ingestion_run_id: str
    chunk_strategy: str
    chunk_strategy_version: str
    processing_status: str = "completed"


class ArtifactPayload(BaseModel):
    artifact_id: str
    artifact_type: str
    schema_version: str
    strategy_version: str
    content: str
    document: DocumentMetadata
    lineage: LineageMetadata
    processing: ProcessingMetadata
    extension: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_artifact_type_and_extension(self) -> "ArtifactPayload":
        if self.artifact_type not in ARTIFACT_TYPES:
            raise ValueError(f"unsupported artifact_type: {self.artifact_type}")

        required = REQUIRED_EXTENSION_FIELDS[self.artifact_type]
        missing = sorted(field for field in required if field not in self.extension)
        if missing:
            raise ValueError(
                f"extension missing required fields for {self.artifact_type}: {', '.join(missing)}"
            )
        return self


def validate_payload(payload: dict[str, Any]) -> tuple[bool, list[dict[str, Any]]]:
    try:
        ArtifactPayload.model_validate(payload)
        return True, []
    except ValidationError as exc:
        return False, exc.errors()
