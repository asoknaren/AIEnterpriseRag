from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_id: str
    source_uri: str
    source_type: str
    content: str


class DocumentUpdateRequest(BaseModel):
    source_uri: str | None = None
    source_type: str | None = None
    content: str | None = None
    expected_version: int


class DocumentResponse(BaseModel):
    document_id: str
    source_uri: str | None = None
    source_type: str | None = None
    content: str | None = None
    version: int = 1
    status: str = Field(default="accepted")


class ArtifactRequest(BaseModel):
    artifact_id: str
    document_id: str
    artifact_type: str
    content: str


class ArtifactUpdateRequest(BaseModel):
    artifact_type: str | None = None
    content: str | None = None
    expected_version: int


class ArtifactResponse(BaseModel):
    artifact_id: str
    document_id: str | None = None
    artifact_type: str | None = None
    content: str | None = None
    version: int = 1
    status: str = Field(default="accepted")


class EmbeddingUpsertItem(BaseModel):
    artifact_id: str
    document_id: str
    artifact_type: str
    content: str
    metadata: dict = Field(default_factory=dict)
    lineage: dict = Field(default_factory=dict)


class EmbeddingUpsertRequest(BaseModel):
    items: list[EmbeddingUpsertItem]


class EmbeddingUpsertResponse(BaseModel):
    accepted: int
    model_provider: str
    model_name: str


class SearchRequest(BaseModel):
    query_text: str
    top_k: int = 5
    filters: dict = Field(default_factory=dict)


class SearchResult(BaseModel):
    artifact_id: str
    score: float
    artifact_type: str | None = None
    document_id: str | None = None
    content: str | None = None
    metadata: dict = Field(default_factory=dict)
    lineage: dict = Field(default_factory=dict)


class SearchResponse(BaseModel):
    items: list[SearchResult]
