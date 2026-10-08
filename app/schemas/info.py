"""Pydantic schemas for the info endpoint."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AppInfo(BaseModel):
    """Basic application information returned by GET /api/v1/info."""

    name: str = Field(..., description="Nombre del proyecto.")
    version: str = Field(..., description="Versión semántica del proyecto.")
    environment: str = Field(..., description="Entorno actual (development, staging, ...).")
    llm_enabled: bool = Field(
        ...,
        description="Indica si el proyecto ya tiene un LLM real integrado.",
    )
