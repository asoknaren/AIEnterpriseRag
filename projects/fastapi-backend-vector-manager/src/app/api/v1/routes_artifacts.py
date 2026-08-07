from __future__ import annotations

from fastapi import APIRouter, Request

from app.models.contracts import ArtifactRequest, ArtifactResponse, ArtifactUpdateRequest

router = APIRouter(prefix="/api/v1/artifacts", tags=["artifacts"])


@router.post("", response_model=ArtifactResponse)
def create_artifact(payload: ArtifactRequest, request: Request) -> ArtifactResponse:
    record = request.app.state.repository.create_artifact(payload.model_dump())
    return ArtifactResponse(**record)


@router.get("/{artifact_id}", response_model=ArtifactResponse)
def get_artifact(artifact_id: str, request: Request) -> ArtifactResponse:
    record = request.app.state.repository.get_artifact(artifact_id)
    return ArtifactResponse(**{**record, "status": "resolved"})


@router.put("/{artifact_id}", response_model=ArtifactResponse)
def update_artifact(artifact_id: str, payload: ArtifactUpdateRequest, request: Request) -> ArtifactResponse:
    record = request.app.state.repository.update_artifact(artifact_id, payload.model_dump())
    return ArtifactResponse(**record)


@router.delete("/{artifact_id}", response_model=ArtifactResponse)
def delete_artifact(artifact_id: str, request: Request) -> ArtifactResponse:
    record = request.app.state.repository.delete_artifact(artifact_id)
    return ArtifactResponse(**record)
