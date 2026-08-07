from __future__ import annotations

from fastapi import HTTPException

from app.storage.in_memory_db import InMemoryDatabase
from app.storage.transactions import transaction


class Repository:
    def __init__(self, db: InMemoryDatabase) -> None:
        self.db = db

    def create_document(self, payload: dict) -> dict:
        with transaction(self.db):
            doc_id = payload["document_id"]
            version = 1
            record = {
                "document_id": doc_id,
                "source_uri": payload["source_uri"],
                "source_type": payload["source_type"],
                "content": payload["content"],
                "version": version,
                "status": "accepted",
            }
            self.db.documents[doc_id] = record
            return record

    def get_document(self, document_id: str) -> dict:
        if document_id not in self.db.documents:
            raise HTTPException(status_code=404, detail="document not found")
        return self.db.documents[document_id]

    def update_document(self, document_id: str, payload: dict) -> dict:
        with transaction(self.db):
            current = self.get_document(document_id)
            expected = payload["expected_version"]
            if current["version"] != expected:
                raise HTTPException(status_code=409, detail="version conflict")
            updated = {**current}
            for field in ("source_uri", "source_type", "content"):
                if payload.get(field) is not None:
                    updated[field] = payload[field]
            updated["version"] = current["version"] + 1
            updated["status"] = "updated"
            self.db.documents[document_id] = updated
            return updated

    def delete_document(self, document_id: str) -> dict:
        with transaction(self.db):
            _ = self.get_document(document_id)
            self.db.documents.pop(document_id, None)
            artifact_ids = [aid for aid, item in self.db.artifacts.items() if item.get("document_id") == document_id]
            for aid in artifact_ids:
                self.db.artifacts.pop(aid, None)
            return {"document_id": document_id, "status": "deleted", "version": 1}

    def create_artifact(self, payload: dict) -> dict:
        with transaction(self.db):
            artifact_id = payload["artifact_id"]
            record = {
                "artifact_id": artifact_id,
                "document_id": payload["document_id"],
                "artifact_type": payload["artifact_type"],
                "content": payload["content"],
                "version": 1,
                "status": "accepted",
            }
            self.db.artifacts[artifact_id] = record
            return record

    def get_artifact(self, artifact_id: str) -> dict:
        if artifact_id not in self.db.artifacts:
            raise HTTPException(status_code=404, detail="artifact not found")
        return self.db.artifacts[artifact_id]

    def update_artifact(self, artifact_id: str, payload: dict) -> dict:
        with transaction(self.db):
            current = self.get_artifact(artifact_id)
            expected = payload["expected_version"]
            if current["version"] != expected:
                raise HTTPException(status_code=409, detail="version conflict")
            updated = {**current}
            for field in ("artifact_type", "content"):
                if payload.get(field) is not None:
                    updated[field] = payload[field]
            updated["version"] = current["version"] + 1
            updated["status"] = "updated"
            self.db.artifacts[artifact_id] = updated
            return updated

    def delete_artifact(self, artifact_id: str) -> dict:
        with transaction(self.db):
            _ = self.get_artifact(artifact_id)
            self.db.artifacts.pop(artifact_id, None)
            return {"artifact_id": artifact_id, "status": "deleted", "version": 1}
