"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure project root is on sys.path so `app` is importable from tests.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app  # noqa: E402


@pytest.fixture()
def client() -> TestClient:
    """Return a FastAPI TestClient bound to a fresh app instance.

    Using TestClient (which internally drives the ASGI app with httpx) keeps
    integration tests hermetic: no real HTTP server needs to be running.
    """
    return TestClient(app)
