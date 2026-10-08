"""Pydantic schemas for the health endpoint."""
from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check payload returned by GET /health."""

    status: str = Field(..., description="Estado del servicio (ok/degraded/down).")
    service: str = Field(..., description="Nombre del servicio.")
    version: str = Field(..., description="Versión del servicio.")
