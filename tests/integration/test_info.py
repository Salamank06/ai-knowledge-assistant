"""T-05: GET /api/v1/info contract."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_info_returns_metadata_and_llm_disabled(client: TestClient) -> None:
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "AI Knowledge Assistant"
    assert payload["version"] == "0.1.0"
    assert payload["environment"] == "development"
    assert payload["llm_enabled"] is False
