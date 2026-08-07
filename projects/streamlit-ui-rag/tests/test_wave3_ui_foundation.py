from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from app_logic import transition_trace
from client import FastApiSearchClient
from ui_state import UIState, build_default_ui_state


def test_ui_smoke_expected_controls_render_in_default_state():
    state = build_default_ui_state()
    assert isinstance(state, UIState)
    assert state.controls.top_k == 5
    assert state.controls.strategy_filter == "all"
    assert state.controls.source_filter == "all"


def test_submit_action_transitions_loading_then_response_or_error():
    state = build_default_ui_state()
    state.controls.query_text = "azure"

    client = FastApiSearchClient(lambda _payload: {"items": [{"artifact_id": "a-1", "score": 0.9, "content": "x"}]})
    trace = transition_trace(state, client)

    assert trace[0]["loading"] is False
    assert trace[1]["loading"] is True
    assert trace[2]["loading"] is False
    assert trace[2]["result_count"] == 1
