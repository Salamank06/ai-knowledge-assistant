"""T-02: GET /health must return HTTP 200."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "AI Knowledge Assistant"
    assert payload["version"] == "0.1.0"
