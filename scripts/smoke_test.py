"""Quick smoke test against a running uvicorn instance.

Usage:
    python scripts/smoke_test.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"


def main() -> int:
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        health = client.get("/health")
        info = client.get("/api/v1/info")
        ok_chat = client.post("/api/v1/chat", json={"question": "¿Qué es FastAPI?"})
        bad_chat = client.post("/api/v1/chat", json={"question": "ab"})

    print("[smoke] GET /health          ->", health.status_code, health.json())
    print("[smoke] GET /api/v1/info     ->", info.status_code, info.json())
    print("[smoke] POST /chat (válido)  ->", ok_chat.status_code, ok_chat.json())
    print("[smoke] POST /chat (corto)   ->", bad_chat.status_code, bad_chat.json())

    assert health.status_code == 200
    assert info.status_code == 200 and info.json()["llm_enabled"] is False
    assert ok_chat.status_code == 200 and ok_chat.json()["provider"] == "bootstrap-local"
    assert bad_chat.status_code == 422
    print("[smoke] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
