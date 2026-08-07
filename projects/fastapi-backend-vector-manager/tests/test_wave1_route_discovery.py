from __future__ import annotations

from conftest import make_client


def test_wave1_baseline_routes_are_registered():
    client = make_client()

    create_document = client.post(
        "/api/v1/documents",
        json={
            "document_id": "doc-routes",
            "source_uri": "https://example.com/r.md",
            "source_type": "markdown",
            "content": "sample",
        },
    )
    assert create_document.status_code == 200

    get_document = client.get("/api/v1/documents/doc-routes")
    assert get_document.status_code == 200

    create_artifact = client.post(
        "/api/v1/artifacts",
        json={
            "artifact_id": "art-routes",
            "document_id": "doc-routes",
            "artifact_type": "semantic_chunk",
            "content": "artifact",
        },
    )
    assert create_artifact.status_code == 200

    get_artifact = client.get("/api/v1/artifacts/art-routes")
    assert get_artifact.status_code == 200

    mode = client.get("/api/v1/ops/mode")
    assert mode.status_code == 200
