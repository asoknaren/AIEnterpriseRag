from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from bridge.fastapi_payload_mapper import map_bundle_to_fastapi_payload
from contracts.field_parity import missing_required_metadata_fields


def test_mapped_payload_preserves_required_metadata_fields():
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "p1_bundle_valid.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    mapped = map_bundle_to_fastapi_payload(payload)

    for artifact in mapped["artifacts"]:
        missing = missing_required_metadata_fields(artifact["metadata"])
        assert missing == []
