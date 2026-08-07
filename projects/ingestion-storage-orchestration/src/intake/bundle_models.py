from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class IngestArtifact(BaseModel):
    artifact_id: str
    artifact_type: str
    content: str
    document_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    lineage: dict[str, Any] = Field(default_factory=dict)


class IngestBundle(BaseModel):
    run_id: str
    document_id: str
    artifacts: list[IngestArtifact]
