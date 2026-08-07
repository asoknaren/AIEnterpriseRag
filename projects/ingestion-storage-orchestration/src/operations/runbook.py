from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SLOTargets:
    success_rate: float
    p95_latency_seconds: float
    duplicate_write_rate: float


DEFAULT_SLOS = SLOTargets(
    success_rate=0.99,
    p95_latency_seconds=2.0,
    duplicate_write_rate=0.0,
)


def build_runbook() -> str:
    return "\n".join(
        [
            "Ingestion Runbook (Wave 4 RC)",
            "1) Validate bundle schema before submission.",
            "2) Execute idempotent submission plan.",
            "3) On interruption, resume from saved run state.",
            "4) Verify no duplicate active records post-recovery.",
        ]
    )
