from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/v1/ops", tags=["ops"])


@router.get("/mode")
def active_mode(request: Request) -> dict[str, str | list[str]]:
    return {
        "active_mode": request.app.state.active_mode,
        "adapters": request.app.state.adapters,
    }
