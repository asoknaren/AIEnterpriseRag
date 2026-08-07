from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from intake.bundle_validator import validate_bundle


def test_invalid_bundle_returns_indexed_errors():
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "p1_bundle_invalid.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    is_valid, errors = validate_bundle(payload)

    assert not is_valid
    assert any("artifacts.0.content" in message for message in errors)
