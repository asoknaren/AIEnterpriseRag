from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from integration.fastapi_client import FastApiStorageClient
from integration.reprocessing import detect_orphaned_records, plan_reprocessing


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict]] = []

    def __call__(self, method: str, path: str, json: dict):
        self.calls.append((method, path, json))
        return {"status": "ok", "method": method, "path": path, "payload": json}


def test_contract_integration_mock_for_create_update_delete_and_reprocess():
    transport = FakeTransport()
    client = FastApiStorageClient(transport)

    client.create_document(
        {
            "document_id": "doc-1",
            "source_uri": "s://a",
            "source_type": "pdf",
            "content": "alpha",
        }
    )
    client.update_document(
        "doc-1",
        {
            "source_uri": "s://b",
            "source_type": "pdf",
            "content": "alpha beta",
            "expected_version": 1,
        },
    )
    client.delete_document("doc-1")

    artifacts = [
        {
            "artifact_id": "a-1",
            "document_id": "doc-1",
            "artifact_type": "semantic_chunk",
            "content": "alpha",
            "metadata": {"chunk_strategy_version": "3.0.0"},
            "lineage": {},
        }
    ]
    updated = plan_reprocessing(artifacts, "4.0.0")
    client.upsert_embedding_batch(updated)

    assert transport.calls[0][0] == "POST"
    assert transport.calls[1][0] == "PUT"
    assert transport.calls[2][0] == "DELETE"
    assert transport.calls[3][1] == "/api/v1/embeddings/upsert"
    assert updated[0]["metadata"]["chunk_strategy_version"] == "4.0.0"


def test_reprocessing_completes_without_orphaned_state():
    existing_ids = {"a-1", "a-2"}
    submitted = [{"artifact_id": "a-1"}, {"artifact_id": "a-2"}]

    orphans = detect_orphaned_records(existing_ids, submitted)
    assert orphans == []
