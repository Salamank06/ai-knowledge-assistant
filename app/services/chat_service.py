"""Bootstrap chat service.

This service is intentionally simple: it does NOT call any LLM. It returns
a deterministic, helpful response so the API can be exercised end-to-end
and later swapped for a real model integration without changing the router
contract.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from app.config import settings


@dataclass(frozen=True)
class ChatResult:
    """Internal representation of a chat response.

    Keeping this as a dataclass (rather than a Pydantic model) makes the
    service independent of HTTP-layer types. The router converts it to
    the public schema.
    """

    answer: str
    provider: str


class ChatService:
    """Service responsible for producing chat answers.

    The bootstrap implementation returns a structured, echo-style answer
    that makes it obvious the request was processed but no LLM was called.
    """

    def __init__(self, provider_name: str | None = None) -> None:
        self._provider_name = provider_name or settings.provider_name

    async def ask(self, question: str) -> ChatResult:
        """Generate a bootstrap answer for the given question.

        The call is `async` to mirror the real-world call shape that will be
        used when an LLM provider is integrated in later modules. The
        internal logic stays deterministic and side-effect free.
        """
        # Tiny async sleep to demonstrate the event loop is non-blocking
        # and to simulate a non-trivial handler without coupling to any LLM.
        await asyncio.sleep(0)

        cleaned = question.strip()
        preview = cleaned if len(cleaned) <= 120 else cleaned[:117] + "..."
        answer = (
            "[bootstrap-local] Recibí tu pregunta. "
            f"Esta es una respuesta de marcador de posición (sin LLM). "
            f"Pregunta registrada: \"{preview}\""
        )
        return ChatResult(answer=answer, provider=self._provider_name)
