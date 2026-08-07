from __future__ import annotations

from conftest import make_client


def _seed_document_and_vector(client):
    create_doc = client.post(
        "/api/v1/documents",
        json={
            "document_id": "doc-401",
            "source_uri": "s://doc-401",
            "source_type": "pdf",
            "content": "alpha architecture",
        },
    )
    assert create_doc.status_code == 200

    upsert = client.post(
        "/api/v1/embeddings/upsert",
        json={
            "items": [
                {
                    "artifact_id": "art-401",
                    "document_id": "doc-401",
                    "artifact_type": "semantic_chunk",
                    "content": "alpha architecture",
                    "metadata": {
                        "chunk_strategy": "semantic_chunk",
                        "source_type": "pdf",
                        "source_uri": "s://doc-401",
                        "chunk_strategy_version": "4.0.0",
                    },
                    "lineage": {"source_ref": "sec-1"},
                }
            ]
        },
    )
    assert upsert.status_code == 200


def test_health_and_readiness_endpoints_and_telemetry_smoke():
    client = make_client()

    health = client.get("/api/v1/health")
    readiness = client.get("/api/v1/readiness")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert readiness.status_code == 200
    assert readiness.json()["status"] in {"ready", "degraded"}

    _ = client.get("/api/v1/ops/mode")
    assert client.app.state.telemetry.events
    event = client.app.state.telemetry.events[-1]
    assert "trace_id" in event
    assert "endpoint" in event
    assert "latency_ms" in event
    assert "outcome" in event


def test_ingestion_status_lookup_roundtrip():
    client = make_client()

    missing = client.get("/api/v1/ingestion/status/run-x")
    assert missing.status_code == 200
    assert missing.json()["status"] == "not_found"

    set_state = client.post("/api/v1/ingestion/status/run-x/running")
    assert set_state.status_code == 200

    found = client.get("/api/v1/ingestion/status/run-x")
    assert found.json()["status"] == "running"


def test_end_to_end_interoperability_create_search_update_delete():
    client = make_client()
    _seed_document_and_vector(client)

    search = client.post("/api/v1/search/similarity", json={"query_text": "architecture", "top_k": 3, "filters": {}})
    assert search.status_code == 200
    assert search.json()["items"]

    update = client.put(
        "/api/v1/documents/doc-401",
        json={"source_uri": "s://doc-401-v2", "source_type": "pdf", "content": "alpha architecture beta", "expected_version": 1},
    )
    assert update.status_code == 200

    delete = client.delete("/api/v1/documents/doc-401")
    assert delete.status_code == 200


def test_mode_parity_matrix_for_supported_expectations(monkeypatch):
    from fastapi.testclient import TestClient

    from app.main import create_app

    for profile in ["postgres-only", "qdrant-only", "combined"]:
        monkeypatch.setenv("APP_PROFILE", profile)
        app = create_app()
        client = TestClient(app)
        mode = client.get("/api/v1/ops/mode")
        assert mode.status_code == 200
        assert mode.json()["active_mode"] == profile
