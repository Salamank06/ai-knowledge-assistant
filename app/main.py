"""FastAPI application entry point.

This module wires routers, exposes OpenAPI/Swagger under /docs and /redoc
(RF-09), and provides a `create_app` factory so tests can build a fresh
instance without depending on a running server.
"""
from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import chat, health, info
from app.config import settings


def create_app() -> FastAPI:
    """Application factory.

    Using a factory keeps the global module state minimal, makes test
    isolation straightforward, and lets us extend the app later without
    breaking existing imports.
    """
    application = FastAPI(
        title=settings.name,
        version=settings.version,
        description=(
            "Bootstrap API for the AI Knowledge Assistant. "
            "In this increment (Module 0) no LLM provider is integrated; "
            "the chat endpoint returns a deterministic local response."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.include_router(health.router)
    application.include_router(chat.router)
    application.include_router(info.router)

    return application


app = create_app()
