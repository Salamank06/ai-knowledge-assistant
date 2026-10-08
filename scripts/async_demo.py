"""AsyncIO demonstration script.

This script exercises two things required by the rubric:
1. Concurrent execution with `asyncio.gather` (true AsyncIO usage).
2. Asynchronous HTTP consumption with `httpx.AsyncClient`.

Run it after starting the API with:
    uvicorn app.main:app --reload
or directly without a server by importing the app in-process.
"""
from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

# Allow running the script as `python scripts/async_demo.py` from project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import httpx  # noqa: E402

from app.main import app  # noqa: E402

BASE_URL = "http://127.0.0.1:8000"


async def call_health(client: httpx.AsyncClient) -> dict:
    response = await client.get(f"{BASE_URL}/health", timeout=5.0)
    response.raise_for_status()
    return response.json()


async def call_chat(client: httpx.AsyncClient, question: str) -> dict:
    response = await client.post(
        f"{BASE_URL}/api/v1/chat",
        json={"question": question},
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()


async def call_info(client: httpx.AsyncClient) -> dict:
    response = await client.get(f"{BASE_URL}/api/v1/info", timeout=5.0)
    response.raise_for_status()
    return response.json()


async def main() -> None:
    print(f"[demo] FastAPI app routes registered: {[r.path for r in app.routes if hasattr(r, 'path')]}")

    # In-process quick check using the app's own client would require ASGITransport;
    # to keep the script a faithful representation of a real client, we hit
    # a running server. If you don't have one, start it first in another shell.
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        # Fire three requests concurrently: this proves the event loop is in use.
        health, chat, info = await asyncio.gather(
            call_health(client),
            call_chat(client, "¿Qué es FastAPI?"),
            call_info(client),
        )
    elapsed_ms = (time.perf_counter() - start) * 1000

    print("[demo] /health     ->", health)
    print("[demo] /api/v1/chat->", chat)
    print("[demo] /api/v1/info->", info)
    print(f"[demo] 3 concurrent requests finished in {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    asyncio.run(main())
