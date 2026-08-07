from __future__ import annotations

from conftest import make_client


def _seed_vectors(client):
    payload = {
        "items": [
            {
                "artifact_id": "seed-1",
                "document_id": "doc-601",
                "artifact_type": "semantic_chunk",
                "content": "azure platform architecture",
                "metadata": {"chunk_strategy": "semantic_chunk", "source_type": "markdown", "source_uri": "s://1", "chunk_strategy_version": "3.0.0", "strategy": "semantic"},
                "lineage": {"source_ref": "md:1"},
            },
            {
                "artifact_id": "seed-2",
                "document_id": "doc-602",
                "artifact_type": "contextual_chunk",
                "content": "federal compliance controls",
                "metadata": {"chunk_strategy": "contextual_chunk", "source_type": "markdown", "source_uri": "s://2", "chunk_strategy_version": "3.0.0", "strategy": "contextual"},
                "lineage": {"source_ref": "md:2"},
            },
            {
                "artifact_id": "seed-3",
                "document_id": "doc-603",
                "artifact_type": "semantic_chunk",
                "content": "azure architecture reference",
                "metadata": {"chunk_strategy": "semantic_chunk", "source_type": "markdown", "source_uri": "s://3", "chunk_strategy_version": "3.0.0", "strategy": "semantic"},
                "lineage": {"source_ref": "md:3"},
            },
        ]
    }
    response = client.post("/api/v1/embeddings/upsert", json=payload)
    assert response.status_code == 200


def test_vector_upsert_and_delete_behavior():
    client = make_client()
    _seed_vectors(client)

    baseline = client.post("/api/v1/search/similarity", json={"query_text": "azure architecture", "top_k": 5, "filters": {}})
    assert any(item["artifact_id"] == "seed-1" for item in baseline.json()["items"])

    client.app.state.vector_adapter.delete("seed-1")

    after_delete = client.post("/api/v1/search/similarity", json={"query_text": "azure architecture", "top_k": 5, "filters": {}})
    assert all(item["artifact_id"] != "seed-1" for item in after_delete.json()["items"])


def test_retrieval_endpoints_relevance_and_filter_correctness():
    client = make_client()
    _seed_vectors(client)

    relevance = client.post("/api/v1/search/similarity", json={"query_text": "azure architecture", "top_k": 2, "filters": {}})
    assert relevance.status_code == 200
    top_ids = [item["artifact_id"] for item in relevance.json()["items"]]
    assert "seed-1" in top_ids or "seed-3" in top_ids

    filtered = client.post(
        "/api/v1/search/filter",
        json={"query_text": "architecture", "top_k": 5, "filters": {"artifact_type": "contextual_chunk"}},
    )
    assert filtered.status_code == 200
    assert filtered.json()["items"]
    assert all(item["artifact_type"] == "contextual_chunk" for item in filtered.json()["items"])
