from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from app_logic import submit_query, submit_query_with_degradation_handling
from client import FastApiSearchClient
from ui_state import build_default_ui_state


def test_live_integration_path_expected_top_k_behavior():
    state = build_default_ui_state()
    state.controls.query_text = "azure"
    state.controls.top_k = 2

    client = FastApiSearchClient(
        lambda payload: {
            "items": [
                {"artifact_id": "a-1", "score": 0.9, "artifact_type": "semantic_chunk", "document_id": "d1", "content": "azure architecture"},
                {"artifact_id": "a-2", "score": 0.8, "artifact_type": "semantic_chunk", "document_id": "d2", "content": "azure controls"},
                {"artifact_id": "a-3", "score": 0.2, "artifact_type": "contextual_chunk", "document_id": "d3", "content": "misc"},
            ][: payload["top_k"]]
        }
    )

    next_state = submit_query(state, client)
    assert len(next_state.results) == 2
    assert next_state.results[0]["score"] >= next_state.results[1]["score"]


def test_degradation_state_has_clear_user_messaging():
    state = build_default_ui_state()

    client = FastApiSearchClient(lambda _payload: (_ for _ in ()).throw(RuntimeError("backend degraded due to dependency outage")))
    degraded = submit_query_with_degradation_handling(state, client)

    assert degraded.error is not None
    assert "Service degraded" in degraded.error
