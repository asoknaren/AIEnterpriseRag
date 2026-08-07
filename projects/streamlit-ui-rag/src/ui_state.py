from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QueryControls:
    query_text: str = ""
    top_k: int = 5
    strategy_filter: str = "all"
    source_filter: str = "all"


@dataclass
class UIState:
    controls: QueryControls = field(default_factory=QueryControls)
    loading: bool = False
    error: str | None = None
    results: list[dict[str, Any]] = field(default_factory=list)


def build_default_ui_state() -> UIState:
    return UIState()


def serialize_query_request(state: UIState) -> dict[str, Any]:
    filters: dict[str, Any] = {}
    if state.controls.strategy_filter != "all":
        filters["artifact_type"] = state.controls.strategy_filter
    if state.controls.source_filter != "all":
        filters["source_type"] = state.controls.source_filter

    return {
        "query_text": state.controls.query_text,
        "top_k": state.controls.top_k,
        "filters": filters,
    }
