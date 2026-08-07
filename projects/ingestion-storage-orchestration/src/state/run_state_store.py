from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RunState:
    run_id: str
    document_id: str
    status: str = "started"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InMemoryRunStateStore:
    def __init__(self) -> None:
        self._states: dict[str, RunState] = {}

    def create(self, run_id: str, document_id: str) -> RunState:
        state = RunState(run_id=run_id, document_id=document_id)
        self._states[run_id] = state
        return state

    def update_status(self, run_id: str, status: str) -> RunState:
        state = self._states[run_id]
        state.status = status
        return state

    def get(self, run_id: str) -> RunState | None:
        return self._states.get(run_id)
