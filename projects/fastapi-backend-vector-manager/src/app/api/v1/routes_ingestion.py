from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/v1/ingestion", tags=["ingestion"])


@router.get("/status/{run_id}")
def ingestion_status(run_id: str, request: Request) -> dict:
    state = request.app.state.ingestion_status.get(run_id)
    if state is None:
        return {"run_id": run_id, "status": "not_found"}
    return {"run_id": run_id, "status": state}


@router.post("/status/{run_id}/{status}")
def update_ingestion_status(run_id: str, status: str, request: Request) -> dict:
    request.app.state.ingestion_status[run_id] = status
    return {"run_id": run_id, "status": status}
