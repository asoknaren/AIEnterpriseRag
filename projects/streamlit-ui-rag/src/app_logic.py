from __future__ import annotations

from typing import Any

from client import FastApiSearchClient
from rendering import render_ranked_results
from ui_state import UIState, serialize_query_request


def submit_query(state: UIState, client: FastApiSearchClient) -> UIState:
    next_state = UIState(controls=state.controls, loading=True, error=None, results=[])
    payload = serialize_query_request(next_state)

    try:
        response = client.search(payload)
    except Exception as exc:
        return UIState(controls=state.controls, loading=False, error=str(exc), results=[])

    rendered = render_ranked_results(response.get("items", []))
    return UIState(controls=state.controls, loading=False, error=None, results=rendered)


def transition_trace(state: UIState, client: FastApiSearchClient) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = [{"loading": state.loading, "error": state.error, "result_count": len(state.results)}]
    loading_state = UIState(controls=state.controls, loading=True, error=None, results=[])
    trace.append({"loading": loading_state.loading, "error": loading_state.error, "result_count": len(loading_state.results)})

    final_state = submit_query(state, client)
    trace.append({"loading": final_state.loading, "error": final_state.error, "result_count": len(final_state.results)})
    return trace
