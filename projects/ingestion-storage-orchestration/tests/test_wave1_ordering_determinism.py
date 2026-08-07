from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from bridge.fastapi_payload_mapper import map_bundle_to_fastapi_payload


def test_mapping_order_is_deterministic_for_identical_inputs():
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "p1_bundle_valid.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    mapped_1 = map_bundle_to_fastapi_payload(payload)
    mapped_2 = map_bundle_to_fastapi_payload(payload)

    ids_1 = [item["artifact_id"] for item in mapped_1["artifacts"]]
    ids_2 = [item["artifact_id"] for item in mapped_2["artifacts"]]

    assert ids_1 == ids_2
