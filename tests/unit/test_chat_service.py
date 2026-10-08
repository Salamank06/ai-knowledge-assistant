"""T-01: Unit test for the chat service."""
from __future__ import annotations

import pytest

from app.services.chat_service import ChatService


@pytest.mark.asyncio
async def test_chat_service_responds_to_known_question() -> None:
    """The service must produce a non-empty answer and identify the provider."""
    service = ChatService()
    result = await service.ask("¿Qué es FastAPI?")

    assert result.answer
    assert "bootstrap" in result.answer.lower()
    assert "¿Qué es FastAPI?" in result.answer
    assert result.provider == "bootstrap-local"


@pytest.mark.asyncio
async def test_chat_service_trims_whitespace() -> None:
    """Leading/trailing whitespace must not break the answer preview."""
    service = ChatService()
    result = await service.ask("   Hola mundo   ")
    assert result.answer
    assert "Hola mundo" in result.answer
    assert result.provider == "bootstrap-local"
