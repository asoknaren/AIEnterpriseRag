from __future__ import annotations

from conftest import make_client


def test_operational_mode_endpoint_reports_active_profile(monkeypatch):
    monkeypatch.setenv("APP_PROFILE", "combined")
    client = make_client()

    response = client.get("/api/v1/ops/mode")

    assert response.status_code == 200
    body = response.json()
    assert body["active_mode"] == "combined"
    assert set(body["adapters"]) == {"postgres", "qdrant"}
