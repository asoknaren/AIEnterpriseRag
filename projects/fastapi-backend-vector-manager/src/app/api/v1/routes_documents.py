from __future__ import annotations

from fastapi import APIRouter

from app.models.contracts import DocumentRequest, DocumentResponse

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse)
def create_document(payload: DocumentRequest) -> DocumentResponse:
    return DocumentResponse(document_id=payload.document_id)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str) -> DocumentResponse:
    return DocumentResponse(document_id=document_id, status="resolved")
