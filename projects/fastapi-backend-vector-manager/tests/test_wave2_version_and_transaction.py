from __future__ import annotations

from pathlib import Path
import sys

from conftest import make_client

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from app.storage.in_memory_db import InMemoryDatabase
from app.storage.transactions import transaction


def test_version_conflict_returns_409():
    client = make_client()

    client.post(
        "/api/v1/documents",
        json={
            "document_id": "doc-301",
            "source_uri": "https://example.com/doc-301.md",
            "source_type": "markdown",
            "content": "content v1",
        },
    )

    response = client.put(
        "/api/v1/documents/doc-301",
        json={"content": "content v2", "expected_version": 999},
    )
    assert response.status_code == 409


def test_transaction_rolls_back_on_error():
    db = InMemoryDatabase()
    db.documents["doc-x"] = {"document_id": "doc-x", "version": 1}

    try:
        with transaction(db):
            db.documents["doc-y"] = {"document_id": "doc-y", "version": 1}
            raise RuntimeError("forced rollback")
    except RuntimeError:
        pass

    assert "doc-y" not in db.documents
    assert "doc-x" in db.documents
