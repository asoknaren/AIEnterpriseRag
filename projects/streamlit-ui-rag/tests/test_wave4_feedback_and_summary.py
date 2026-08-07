from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from app_logic import feedback_summary, mark_feedback
from ui_state import build_default_ui_state


def test_feedback_capture_for_positive_and_negative_marks():
    state = build_default_ui_state()
    state = mark_feedback(state, "a-1", True)
    state = mark_feedback(state, "a-2", False)

    assert len(state.feedback) == 2
    assert state.feedback[0].artifact_id == "a-1"
    assert state.feedback[1].relevant is False


def test_session_summary_counts_and_percentages_are_accurate():
    state = build_default_ui_state()
    state = mark_feedback(state, "a-1", True)
    state = mark_feedback(state, "a-2", False)
    state = mark_feedback(state, "a-3", True)

    summary = feedback_summary(state)
    assert summary["total"] == 3
    assert summary["positives"] == 2
    assert summary["negatives"] == 1
    assert summary["positive_pct"] == 66.67
