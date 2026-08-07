from __future__ import annotations

from fastapi import APIRouter, Request

from app.models.contracts import SearchRequest, SearchResponse, SearchResult

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.post("/similarity", response_model=SearchResponse)
def similarity_search(payload: SearchRequest, request: Request) -> SearchResponse:
    provider = request.app.state.embedding_provider
    adapter = request.app.state.vector_adapter
    query_embedding = provider.embed_text(payload.query_text)
    found = adapter.search(query_embedding=query_embedding, top_k=payload.top_k, filters=payload.filters)

    items = [
        SearchResult(
            artifact_id=item["point_id"],
            score=item["score"],
            artifact_type=item["payload"].get("artifact_type"),
            document_id=item["payload"].get("document_id"),
            content=item["payload"].get("content"),
            metadata=item["payload"].get("metadata", {}),
            lineage=item["payload"].get("lineage", {}),
        )
        for item in found
    ]
    return SearchResponse(items=items)


@router.post("/filter", response_model=SearchResponse)
def filter_search(payload: SearchRequest, request: Request) -> SearchResponse:
    # Use a deterministic query embedding and rely on strict filter matching.
    provider = request.app.state.embedding_provider
    adapter = request.app.state.vector_adapter
    query_embedding = provider.embed_text(payload.query_text)
    found = adapter.search(query_embedding=query_embedding, top_k=payload.top_k, filters=payload.filters)

    items = [
        SearchResult(
            artifact_id=item["point_id"],
            score=item["score"],
            artifact_type=item["payload"].get("artifact_type"),
            document_id=item["payload"].get("document_id"),
            content=item["payload"].get("content"),
            metadata=item["payload"].get("metadata", {}),
            lineage=item["payload"].get("lineage", {}),
        )
        for item in found
    ]
    return SearchResponse(items=items)
