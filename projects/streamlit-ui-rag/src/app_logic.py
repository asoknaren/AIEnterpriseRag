from __future__ import annotations

import json
from typing import Any

from client import FastApiSearchClient
from rendering import render_ranked_results
from ui_state import FeedbackRecord, UIState, serialize_query_request


def submit_query(state: UIState, client: FastApiSearchClient) -> UIState:
    next_state = UIState(
        controls=state.controls,
        loading=True,
        error=None,
        results=[],
        query_history=state.query_history,
        feedback=state.feedback,
        last_export=state.last_export,
    )
    payload = serialize_query_request(next_state)

    try:
        response = client.search(payload)
    except Exception as exc:
        return UIState(
            controls=state.controls,
            loading=False,
            error=str(exc),
            results=[],
            query_history=state.query_history,
            feedback=state.feedback,
            last_export=state.last_export,
        )

    rendered = render_ranked_results(response.get("items", []))
    history = list(state.query_history)
    history.append(payload)
    return UIState(
        controls=state.controls,
        loading=False,
        error=None,
        results=rendered,
        query_history=history,
        feedback=state.feedback,
        last_export=state.last_export,
    )


def transition_trace(state: UIState, client: FastApiSearchClient) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = [{"loading": state.loading, "error": state.error, "result_count": len(state.results)}]
    loading_state = UIState(controls=state.controls, loading=True, error=None, results=[])
    trace.append({"loading": loading_state.loading, "error": loading_state.error, "result_count": len(loading_state.results)})

    final_state = submit_query(state, client)
    trace.append({"loading": final_state.loading, "error": final_state.error, "result_count": len(final_state.results)})
    return trace


def export_response_payload(state: UIState) -> str:
    payload = {
        "results": state.results,
        "query_history": state.query_history,
        "feedback": [{"artifact_id": item.artifact_id, "relevant": item.relevant} for item in state.feedback],
    }
    return json.dumps(payload, sort_keys=True)


def mark_feedback(state: UIState, artifact_id: str, relevant: bool) -> UIState:
    next_feedback = list(state.feedback)
    next_feedback.append(FeedbackRecord(artifact_id=artifact_id, relevant=relevant))
    return UIState(
        controls=state.controls,
        loading=state.loading,
        error=state.error,
        results=state.results,
        query_history=state.query_history,
        feedback=next_feedback,
        last_export=state.last_export,
    )


def feedback_summary(state: UIState) -> dict[str, float | int]:
    total = len(state.feedback)
    positives = sum(1 for item in state.feedback if item.relevant)
    negatives = total - positives
    positive_pct = (positives / total) * 100.0 if total else 0.0
    return {
        "total": total,
        "positives": positives,
        "negatives": negatives,
        "positive_pct": round(positive_pct, 2),
    }


def submit_query_with_degradation_handling(state: UIState, client: FastApiSearchClient) -> UIState:
    result = submit_query(state, client)
    if result.error and "degraded" in result.error.lower():
        return UIState(
            controls=result.controls,
            loading=False,
            error="Service degraded: showing partial results may be unavailable.",
            results=result.results,
            query_history=result.query_history,
            feedback=result.feedback,
            last_export=result.last_export,
        )
    return result
