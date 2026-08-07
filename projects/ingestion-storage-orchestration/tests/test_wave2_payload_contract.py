from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from bridge.fastapi_payload_mapper import map_bundle_to_fastapi_payload
from submission.payload_contract import batch_artifacts, validate_handoff_payload


def test_contract_compliance_without_embedding_fields():
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "p1_bundle_valid.json"
    bundle = json.loads(fixture.read_text(encoding="utf-8"))
    payload = map_bundle_to_fastapi_payload(bundle)

    is_valid, errors = validate_handoff_payload(payload)

    assert is_valid
    assert errors == []


def test_batch_boundaries_are_enforced():
    artifacts = [{"artifact_id": str(i)} for i in range(5)]

    batches = batch_artifacts(artifacts, batch_size=2)
    assert [len(batch) for batch in batches] == [2, 2, 1]
