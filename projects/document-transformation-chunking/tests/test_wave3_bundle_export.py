import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from export_bundle import build_ingestion_bundle
from orchestrator import StrategyOrchestrator


REPO_ROOT = ROOT.parents[1]
PROJECT2_SRC = REPO_ROOT / "projects" / "ingestion-storage-orchestration" / "src"
sys.path.insert(0, str(PROJECT2_SRC.resolve()))

from submission.payload_contract import validate_handoff_payload


def _run_text() -> dict:
    orchestrator = StrategyOrchestrator(timeout_seconds=2.0, retry_attempts=2)
    run = orchestrator.run_document(
        document_id="doc-403",
        text="one two three four five six seven eight nine ten eleven twelve",
    )
    return build_ingestion_bundle(run)


def test_bundle_contract_validates_against_ingestion_handoff_schema():
    bundle = _run_text()
    payload = {
        "run_id": bundle["run_id"],
        "document_id": bundle["document_id"],
        "artifacts": [
            {
                "artifact_id": item["artifact_id"],
                "document_id": item["document_id"],
                "artifact_type": item["artifact_type"],
                "content": item["content"],
                "metadata": item["metadata"],
                "lineage": item["lineage"],
            }
            for item in bundle["artifacts"]
        ],
    }

    is_valid, errors = validate_handoff_payload(payload)
    assert is_valid, json.dumps(errors)


def test_checksum_reproducibility_for_identical_input_and_config():
    bundle_1 = _run_text()
    bundle_2 = _run_text()

    manifest_1 = sorted(bundle_1["manifests"], key=lambda item: item["artifact_id"])
    manifest_2 = sorted(bundle_2["manifests"], key=lambda item: item["artifact_id"])

    assert manifest_1 == manifest_2
