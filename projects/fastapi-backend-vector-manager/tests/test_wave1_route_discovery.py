from __future__ import annotations

from conftest import make_client


def test_wave1_baseline_routes_are_registered():
    client = make_client()

    expected = {
        "/api/v1/documents",
        "/api/v1/documents/{document_id}",
        "/api/v1/artifacts",
        "/api/v1/artifacts/{artifact_id}",
        "/api/v1/ops/mode",
    }

    route_paths = {route.path for route in client.app.routes}
    assert expected.issubset(route_paths)
