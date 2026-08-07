from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from submission.handoff import HandoffPlanner


def test_handoff_planner_emits_actions_and_batches():
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "p1_bundle_valid.json"
    bundle = json.loads(fixture.read_text(encoding="utf-8"))

    result = HandoffPlanner().prepare(bundle, batch_size=1)

    assert result["payload"]["artifacts"]
    assert len(result["actions"]) == len(result["payload"]["artifacts"])
    assert len(result["batches"]) == len(result["payload"]["artifacts"])
