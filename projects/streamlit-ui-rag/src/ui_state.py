from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QueryControls:
    query_text: str = ""
    top_k: int = 5
    strategy_filter: str = "all"
    source_filter: str = "all"
    date_from: str | None = None
    date_to: str | None = None


@dataclass
class FeedbackRecord:
    artifact_id: str
    relevant: bool


@dataclass
class UIState:
    controls: QueryControls = field(default_factory=QueryControls)
    loading: bool = False
    error: str | None = None
    results: list[dict[str, Any]] = field(default_factory=list)
    query_history: list[dict[str, Any]] = field(default_factory=list)
    feedback: list[FeedbackRecord] = field(default_factory=list)
    last_export: str | None = None


def build_default_ui_state() -> UIState:
    return UIState()


def serialize_query_request(state: UIState) -> dict[str, Any]:
    filters: dict[str, Any] = {}
    if state.controls.strategy_filter != "all":
        filters["artifact_type"] = state.controls.strategy_filter
    if state.controls.source_filter != "all":
        filters["source_type"] = state.controls.source_filter
    if state.controls.date_from:
        filters["date_from"] = state.controls.date_from
    if state.controls.date_to:
        filters["date_to"] = state.controls.date_to

    return {
        "query_text": state.controls.query_text,
        "top_k": state.controls.top_k,
        "filters": filters,
    }
