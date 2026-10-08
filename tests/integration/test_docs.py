"""RF-09: OpenAPI documentation must be exposed under /docs."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_swagger_ui_is_served(client: TestClient) -> None:
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_openapi_schema_is_served(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "/health" in schema["paths"]
    assert "/api/v1/chat" in schema["paths"]
    assert "/api/v1/info" in schema["paths"]
