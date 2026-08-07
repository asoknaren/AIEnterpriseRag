from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health")
def health(request: Request) -> dict:
    return {
        "status": "ok",
        "service": "fastapi-backend-vector-manager",
        "active_mode": request.app.state.active_mode,
    }


@router.get("/readiness")
def readiness(request: Request) -> dict:
    vector_ready = request.app.state.vector_adapter is not None
    repo_ready = request.app.state.repository is not None
    status = "ready" if vector_ready and repo_ready else "degraded"
    return {
        "status": status,
        "dependencies": {
            "repository": "ok" if repo_ready else "down",
            "vector_adapter": "ok" if vector_ready else "down",
        },
    }
