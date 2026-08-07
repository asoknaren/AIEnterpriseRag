from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RunMetrics:
    accepted: int = 0
    rejected: int = 0
    retried: int = 0
    persisted: int = 0
    parse_ms: float = 0.0
    validate_ms: float = 0.0
    submit_ms: float = 0.0
    total_ms: float = 0.0


@dataclass
class RunTelemetry:
    run_id: str
    document_id: str
    state: str = "started"
    metrics: RunMetrics = field(default_factory=RunMetrics)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RunTelemetryTracker:
    VALID_STATES = {"started", "in-progress", "partial-failed", "completed", "failed"}

    def __init__(self) -> None:
        self._runs: dict[str, RunTelemetry] = {}

    def start(self, run_id: str, document_id: str) -> RunTelemetry:
        run = RunTelemetry(run_id=run_id, document_id=document_id)
        self._runs[run_id] = run
        return run

    def transition(self, run_id: str, state: str) -> RunTelemetry:
        if state not in self.VALID_STATES:
            raise ValueError(f"invalid state: {state}")
        run = self._runs[run_id]
        run.state = state
        return run

    def increment(self, run_id: str, *, accepted: int = 0, rejected: int = 0, retried: int = 0, persisted: int = 0) -> None:
        run = self._runs[run_id]
        run.metrics.accepted += accepted
        run.metrics.rejected += rejected
        run.metrics.retried += retried
        run.metrics.persisted += persisted

    def set_durations(self, run_id: str, *, parse_ms: float, validate_ms: float, submit_ms: float, total_ms: float) -> None:
        run = self._runs[run_id]
        run.metrics.parse_ms = parse_ms
        run.metrics.validate_ms = validate_ms
        run.metrics.submit_ms = submit_ms
        run.metrics.total_ms = total_ms

    def get(self, run_id: str) -> RunTelemetry:
        return self._runs[run_id]
