"""Application configuration and metadata.

Centralizes static project metadata so routers/services do not hard-code values.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Static settings for the bootstrap API.

    Values are read from environment variables when present, with safe defaults
    aligned to the module 0 contract (no LLM yet).
    """

    name: str = os.getenv("APP_NAME", "AI Knowledge Assistant")
    version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: str = os.getenv("APP_ENV", "development")
    llm_enabled: bool = os.getenv("LLM_ENABLED", "false").lower() in {"1", "true", "yes"}
    provider_name: str = "bootstrap-local"


settings = Settings()
