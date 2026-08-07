from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from submission.idempotency import IdempotencyRegistry, plan_submission_actions


def test_replay_submission_is_idempotent_for_same_artifact():
    registry = IdempotencyRegistry()
    artifact = {
        "artifact_id": "a-1",
        "document_id": "doc-1",
        "artifact_type": "semantic_chunk",
        "content": "same content",
    }

    first = plan_submission_actions([artifact], registry)[0]
    second = plan_submission_actions([artifact], registry)[0]

    assert first.action == "create"
    assert second.action == "skip_duplicate"


def test_changed_artifact_routes_to_update_path():
    registry = IdempotencyRegistry()
    original = {
        "artifact_id": "a-1",
        "document_id": "doc-1",
        "artifact_type": "semantic_chunk",
        "content": "same content",
    }
    changed = {
        "artifact_id": "a-2",
        "document_id": "doc-1",
        "artifact_type": "semantic_chunk",
        "content": "same content",
    }

    _ = plan_submission_actions([original], registry)[0]
    update = plan_submission_actions([changed], registry)[0]

    assert update.action == "update"
