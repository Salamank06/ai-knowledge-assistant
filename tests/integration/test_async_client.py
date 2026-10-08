"""AsyncIO + HTTPX evidence: an async test client driving the FastAPI app."""
from __future__ import annotations

import asyncio

import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_concurrent_requests_via_async_client() -> None:
    """Fire 3 concurrent requests with httpx.AsyncClient to prove async usage."""
    transport = httpx.ASGITransport(app=app)

    async def hit(path: str, payload: dict | None = None) -> httpx.Response:
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as ac:
            if payload is None:
                return await ac.get(path)
            return await ac.post(path, json=payload)

    results = await asyncio.gather(
        hit("/health"),
        hit("/api/v1/chat", {"question": "Hola desde AsyncIO"}),
        hit("/api/v1/info"),
    )

    assert results[0].status_code == 200
    assert results[1].status_code == 200
    assert results[2].status_code == 200
    assert results[1].json()["provider"] == "bootstrap-local"
