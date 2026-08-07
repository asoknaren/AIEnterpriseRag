from __future__ import annotations

from fastapi import APIRouter

from app.models.contracts import ArtifactRequest, ArtifactResponse

router = APIRouter(prefix="/api/v1/artifacts", tags=["artifacts"])


@router.post("", response_model=ArtifactResponse)
def create_artifact(payload: ArtifactRequest) -> ArtifactResponse:
    return ArtifactResponse(artifact_id=payload.artifact_id)


@router.get("/{artifact_id}", response_model=ArtifactResponse)
def get_artifact(artifact_id: str) -> ArtifactResponse:
    return ArtifactResponse(artifact_id=artifact_id, status="resolved")
