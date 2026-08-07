from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from app_logic import export_response_payload, submit_query
from client import FastApiSearchClient
from ui_state import build_default_ui_state, serialize_query_request


def test_filter_mapping_includes_strategy_source_and_date_window():
    state = build_default_ui_state()
    state.controls.query_text = "architecture"
    state.controls.strategy_filter = "semantic_chunk"
    state.controls.source_filter = "pdf"
    state.controls.date_from = "2025-01-01"
    state.controls.date_to = "2025-12-31"

    payload = serialize_query_request(state)
    assert payload["filters"]["artifact_type"] == "semantic_chunk"
    assert payload["filters"]["source_type"] == "pdf"
    assert payload["filters"]["date_from"] == "2025-01-01"
    assert payload["filters"]["date_to"] == "2025-12-31"


def test_query_history_and_export_payload_valid_json():
    state = build_default_ui_state()
    state.controls.query_text = "policy"
    client = FastApiSearchClient(lambda _payload: {"items": [{"artifact_id": "a-1", "score": 0.9, "content": "c"}]})

    next_state = submit_query(state, client)
    assert len(next_state.query_history) == 1

    exported = export_response_payload(next_state)
    parsed = json.loads(exported)
    assert "results" in parsed
    assert "query_history" in parsed
