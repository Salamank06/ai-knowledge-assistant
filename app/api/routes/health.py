"""Health check router (RF-01)."""
from __future__ import annotations

from fastapi import APIRouter

from app.config import settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Liveness check")
async def healthcheck() -> HealthResponse:
    """Return a simple liveness payload.

    This endpoint exists primarily for orchestration platforms (Kubernetes,
    load balancers, uptime monitors) to confirm the process is up and the
    FastAPI app finished wiring.
    """
    return HealthResponse(status="ok", service=settings.name, version=settings.version)
