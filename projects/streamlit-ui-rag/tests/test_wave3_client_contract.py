from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from client import ClientTimeoutError, FastApiSearchClient
from ui_state import build_default_ui_state, serialize_query_request


def test_client_serialization_and_parse_contract():
    state = build_default_ui_state()
    state.controls.query_text = "policy"
    state.controls.top_k = 3
    state.controls.strategy_filter = "semantic_chunk"

    payload = serialize_query_request(state)
    assert payload["query_text"] == "policy"
    assert payload["top_k"] == 3
    assert payload["filters"]["artifact_type"] == "semantic_chunk"

    client = FastApiSearchClient(
        lambda _payload: {
            "items": [
                {"artifact_id": "r-1", "score": 0.8, "artifact_type": "semantic_chunk", "document_id": "doc-1", "content": "text", "metadata": {}, "lineage": {}}
            ]
        }
    )
    response = client.search(payload)
    assert response["items"][0]["artifact_id"] == "r-1"


def test_timeout_and_error_handling_with_retries():
    calls = {"count": 0}

    def transport(_payload):
        calls["count"] += 1
        raise ClientTimeoutError("timeout")

    client = FastApiSearchClient(transport)

    try:
        client.search({"query_text": "x", "top_k": 1, "filters": {}})
        assert False, "expected timeout"
    except ClientTimeoutError:
        pass

    assert calls["count"] == client.config.max_retries
