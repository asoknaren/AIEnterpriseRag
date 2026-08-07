from __future__ import annotations

from fastapi import APIRouter, Request

from app.models.contracts import EmbeddingUpsertRequest, EmbeddingUpsertResponse

router = APIRouter(prefix="/api/v1/embeddings", tags=["embeddings"])


@router.post("/upsert", response_model=EmbeddingUpsertResponse)
def upsert_embeddings(payload: EmbeddingUpsertRequest, request: Request) -> EmbeddingUpsertResponse:
    provider = request.app.state.embedding_provider
    adapter = request.app.state.vector_adapter

    accepted = 0
    for item in payload.items:
        embedding = provider.embed_text(item.content)
        vector_payload = {
            "artifact_id": item.artifact_id,
            "document_id": item.document_id,
            "artifact_type": item.artifact_type,
            "content": item.content,
            "metadata": item.metadata,
            "lineage": item.lineage,
            "model_provider": provider.meta.model_provider,
            "model_name": provider.meta.model_name,
        }
        adapter.upsert(point_id=item.artifact_id, embedding=embedding, payload=vector_payload)
        accepted += 1

    return EmbeddingUpsertResponse(
        accepted=accepted,
        model_provider=provider.meta.model_provider,
        model_name=provider.meta.model_name,
    )
