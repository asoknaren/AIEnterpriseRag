from __future__ import annotations

from typing import Any, Protocol


class HttpTransport(Protocol):
    def __call__(self, method: str, path: str, json: dict[str, Any]) -> dict[str, Any]:
        ...


class FastApiStorageClient:
    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport

    def create_document(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._transport("POST", "/api/v1/documents", payload)

    def update_document(self, document_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._transport("PUT", f"/api/v1/documents/{document_id}", payload)

    def delete_document(self, document_id: str) -> dict[str, Any]:
        return self._transport("DELETE", f"/api/v1/documents/{document_id}", {})

    def upsert_embedding_batch(self, items: list[dict[str, Any]]) -> dict[str, Any]:
        return self._transport("POST", "/api/v1/embeddings/upsert", {"items": items})
