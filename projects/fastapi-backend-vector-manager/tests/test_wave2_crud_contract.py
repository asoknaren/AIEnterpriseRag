from __future__ import annotations

from conftest import make_client


def test_document_and_artifact_crud_lifecycle():
    client = make_client()

    create_doc = client.post(
        "/api/v1/documents",
        json={
            "document_id": "doc-300",
            "source_uri": "https://example.com/doc-300.md",
            "source_type": "markdown",
            "content": "content v1",
        },
    )
    assert create_doc.status_code == 200
    assert create_doc.json()["version"] == 1

    create_artifact = client.post(
        "/api/v1/artifacts",
        json={
            "artifact_id": "art-300",
            "document_id": "doc-300",
            "artifact_type": "semantic_chunk",
            "content": "artifact content",
        },
    )
    assert create_artifact.status_code == 200

    update_doc = client.put(
        "/api/v1/documents/doc-300",
        json={"content": "content v2", "expected_version": 1},
    )
    assert update_doc.status_code == 200
    assert update_doc.json()["version"] == 2

    update_artifact = client.put(
        "/api/v1/artifacts/art-300",
        json={"content": "artifact content v2", "expected_version": 1},
    )
    assert update_artifact.status_code == 200
    assert update_artifact.json()["version"] == 2

    delete_doc = client.delete("/api/v1/documents/doc-300")
    assert delete_doc.status_code == 200
    assert delete_doc.json()["status"] == "deleted"

    get_deleted_artifact = client.get("/api/v1/artifacts/art-300")
    assert get_deleted_artifact.status_code == 404
