"""T-03 / T-04: chat endpoint contract and validation."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_chat_with_valid_question_returns_200(client: TestClient) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"question": "¿Qué es FastAPI?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "bootstrap-local"
    assert payload["answer"]


def test_chat_with_too_short_question_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"question": "ab"},
    )
    assert response.status_code == 422


def test_chat_with_only_spaces_returns_422(client: TestClient) -> None:
    """Pydantic's strip validator must reject whitespace-only input."""
    response = client.post(
        "/api/v1/chat",
        json={"question": "     "},
    )
    assert response.status_code == 422


def test_chat_missing_field_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422
