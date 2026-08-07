from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorEnvelope(BaseModel):
    trace_id: str = Field(..., description="Per-request trace identifier")
    error_code: str
    message: str
    details: list[dict] = Field(default_factory=list)
