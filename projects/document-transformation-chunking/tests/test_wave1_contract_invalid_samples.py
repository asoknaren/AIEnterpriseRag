from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from schema_validator import validate_artifact_payload


def test_missing_required_field_fails_with_indexed_error_message():
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "invalid_missing_required.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    is_valid, errors = validate_artifact_payload(payload)

    assert not is_valid
    assert any("document.document_id" in message for message in errors)
