from __future__ import annotations

from conftest import make_client


def test_invalid_request_body_returns_validation_envelope():
    client = make_client()

    response = client.post("/api/v1/documents", json={"document_id": "doc-1"})

    assert response.status_code == 422
    body = response.json()
    assert body["error_code"] == "request_validation_error"
    assert body["trace_id"]
    assert len(body["details"]) >= 1
