from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_id: str
    source_uri: str
    source_type: str
    content: str


class DocumentResponse(BaseModel):
    document_id: str
    status: str = Field(default="accepted")


class ArtifactRequest(BaseModel):
    artifact_id: str
    document_id: str
    artifact_type: str
    content: str


class ArtifactResponse(BaseModel):
    artifact_id: str
    status: str = Field(default="accepted")
