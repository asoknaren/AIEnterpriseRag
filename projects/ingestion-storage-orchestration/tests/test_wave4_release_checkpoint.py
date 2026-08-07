from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from bridge.fastapi_payload_mapper import map_bundle_to_fastapi_payload
from operations.recovery import ForcedInterruption, execute_with_recovery
from operations.runbook import DEFAULT_SLOS, build_runbook
from submission.payload_contract import validate_handoff_payload


def _bundle() -> dict:
    return {
        "run_id": "run-wave4",
        "document_id": "doc-wave4",
        "artifacts": [
            {
                "artifact_id": "a-1",
                "document_id": "doc-wave4",
                "artifact_type": "semantic_chunk",
                "content": "alpha beta",
                "metadata": {
                    "source_uri": "s://x",
                    "source_type": "pdf",
                    "chunk_strategy": "semantic_chunk",
                    "chunk_strategy_version": "4.0.0",
                },
                "lineage": {"source_ref": "sec-1"},
            }
        ],
    }


def test_end_to_end_dry_run_bundle_to_persistence_payload():
    payload = map_bundle_to_fastapi_payload(_bundle())
    is_valid, errors = validate_handoff_payload(payload)

    assert is_valid, errors


def test_recovery_drill_from_forced_mid_run_interruption():
    artifacts = _bundle()["artifacts"]

    try:
        execute_with_recovery("run-int", "doc-wave4", artifacts, fail_after=0)
    except ForcedInterruption:
        resumed = execute_with_recovery("run-int", "doc-wave4", artifacts, fail_after=None)
        assert resumed["state"] is not None
        assert resumed["state"].status == "completed"
        assert len(resumed["processed"]) == 1
    else:
        assert False, "expected forced interruption"


def test_runbook_and_slo_targets_are_defined_for_release_checkpoint():
    text = build_runbook()
    assert "Ingestion Runbook" in text
    assert DEFAULT_SLOS.success_rate >= 0.99
    assert DEFAULT_SLOS.duplicate_write_rate == 0.0
