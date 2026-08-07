from __future__ import annotations

from conftest import make_client


def test_embedding_contract_and_metadata_capture():
    client = make_client()

    response = client.post(
        "/api/v1/embeddings/upsert",
        json={
            "items": [
                {
                    "artifact_id": "vec-1",
                    "document_id": "doc-501",
                    "artifact_type": "semantic_chunk",
                    "content": "alpha beta gamma",
                    "metadata": {"chunk_strategy": "semantic_chunk", "source_type": "markdown", "source_uri": "s://1", "chunk_strategy_version": "3.0.0"},
                    "lineage": {"source_ref": "md:1"},
                }
            ]
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["accepted"] == 1
    assert body["model_provider"]
    assert body["model_name"]


def test_embedding_determinism_for_unchanged_input():
    client = make_client()
    payload = {
        "items": [
            {
                "artifact_id": "vec-d-1",
                "document_id": "doc-502",
                "artifact_type": "semantic_chunk",
                "content": "same text",
                "metadata": {"chunk_strategy": "semantic_chunk", "source_type": "markdown", "source_uri": "s://2", "chunk_strategy_version": "3.0.0"},
                "lineage": {"source_ref": "md:1"},
            }
        ]
    }

    upsert_1 = client.post("/api/v1/embeddings/upsert", json=payload)
    upsert_2 = client.post("/api/v1/embeddings/upsert", json=payload)
    assert upsert_1.status_code == 200
    assert upsert_2.status_code == 200

    search_1 = client.post("/api/v1/search/similarity", json={"query_text": "same text", "top_k": 5, "filters": {}})
    search_2 = client.post("/api/v1/search/similarity", json={"query_text": "same text", "top_k": 5, "filters": {}})

    assert search_1.status_code == 200
    assert search_2.status_code == 200
    assert [item["artifact_id"] for item in search_1.json()["items"]] == [item["artifact_id"] for item in search_2.json()["items"]]
