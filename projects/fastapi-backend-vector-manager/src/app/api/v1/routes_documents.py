from __future__ import annotations

from fastapi import APIRouter, Request

from app.models.contracts import DocumentRequest, DocumentResponse, DocumentUpdateRequest

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse)
def create_document(payload: DocumentRequest, request: Request) -> DocumentResponse:
    record = request.app.state.repository.create_document(payload.model_dump())
    return DocumentResponse(**record)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, request: Request) -> DocumentResponse:
    record = request.app.state.repository.get_document(document_id)
    return DocumentResponse(**{**record, "status": "resolved"})


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: str, payload: DocumentUpdateRequest, request: Request) -> DocumentResponse:
    record = request.app.state.repository.update_document(document_id, payload.model_dump())
    return DocumentResponse(**record)


@router.delete("/{document_id}", response_model=DocumentResponse)
def delete_document(document_id: str, request: Request) -> DocumentResponse:
    record = request.app.state.repository.delete_document(document_id)
    return DocumentResponse(**record)
