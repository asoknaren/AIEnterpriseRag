from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from schema_validator import validate_artifact_payload


def test_all_valid_contract_samples_pass_validation():
    fixtures = sorted((ROOT / "tests" / "fixtures" / "wave1").glob("valid_*.json"))
    assert len(fixtures) == 6

    for fixture in fixtures:
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        is_valid, errors = validate_artifact_payload(payload)
        assert is_valid, f"{fixture.name} failed: {errors}"
