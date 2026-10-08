"""Pydantic schemas for the chat endpoint."""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """Request payload for POST /api/v1/chat.

    The question must have between 3 and 2000 characters to keep the
    contract clear and to validate boundaries at the edge of the system.
    """

    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Pregunta del usuario (3 a 2000 caracteres).",
        examples=["¿Qué es FastAPI?"],
    )

    @field_validator("question")
    @classmethod
    def _strip_and_require_text(cls, value: str) -> str:
        stripped = value.strip()
        if len(stripped) < 3:
            raise ValueError("La pregunta no puede estar vacía ni tener solo espacios.")
        return stripped


class ChatResponse(BaseModel):
    """Response payload for POST /api/v1/chat.

    `provider` explicitly identifies the bootstrap implementation so clients
    can tell that no real LLM is being invoked.
    """

    answer: str = Field(..., description="Respuesta generada por la capa de servicio.")
    provider: str = Field(
        ...,
        description="Identificador del proveedor (bootstrap-local en Módulo 0).",
    )
