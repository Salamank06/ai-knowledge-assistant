"""Project info router (RF-10)."""
from __future__ import annotations

from fastapi import APIRouter

from app.config import settings
from app.schemas.info import AppInfo

router = APIRouter(prefix="/api/v1", tags=["info"])


@router.get(
    "/info",
    response_model=AppInfo,
    summary="Project metadata",
)
async def info() -> AppInfo:
    """Expose basic project metadata.

    `llm_enabled` is always `false` in Module 0 by design; this field will
    become the single source of truth for clients to detect whether a real
    LLM is wired in later modules.
    """
    return AppInfo(
        name=settings.name,
        version=settings.version,
        environment=settings.environment,
        llm_enabled=settings.llm_enabled,
    )
