"""Chat router (RF-02..RF-08)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api/v1", tags=["chat"])


def get_chat_service() -> ChatService:
    """Dependency provider for the chat service.

    Routers must not instantiate services directly so that the dependency
    graph is explicit and tests can override it easily.
    """
    return ChatService()


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=200,
    summary="Send a question to the bootstrap assistant",
)
async def chat(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Process a chat question through the service layer.

    The router is intentionally thin: it validates input with Pydantic,
    delegates the work to the service, and adapts the result to the
    response schema.
    """
    result = await service.ask(payload.question)
    return ChatResponse(answer=result.answer, provider=result.provider)
