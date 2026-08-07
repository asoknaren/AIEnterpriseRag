from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable


REQUIRED_METADATA_FIELDS = {
    "source_uri",
    "source_type",
    "chunk_strategy",
    "chunk_strategy_version",
}


@dataclass
class QualityReport:
    artifact_count: int
    metadata_completeness: float
    missing_fields: list[str]


def evaluate_metadata_completeness(artifacts: list[dict[str, Any]]) -> QualityReport:
    if not artifacts:
        return QualityReport(artifact_count=0, metadata_completeness=0.0, missing_fields=["no artifacts"])

    missing: list[str] = []
    present_count = 0
    total_expected = len(artifacts) * len(REQUIRED_METADATA_FIELDS)
    for index, artifact in enumerate(artifacts):
        metadata = artifact.get("metadata", {})
        for field in REQUIRED_METADATA_FIELDS:
            if field in metadata and metadata[field] not in (None, ""):
                present_count += 1
            else:
                missing.append(f"artifacts.{index}.metadata.{field}")

    completeness = present_count / total_expected if total_expected else 0.0
    return QualityReport(artifact_count=len(artifacts), metadata_completeness=completeness, missing_fields=missing)


def regression_snapshot(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    for item in artifacts:
        by_type[item.get("artifact_type", "unknown")] = by_type.get(item.get("artifact_type", "unknown"), 0) + 1
    return {"artifact_count": len(artifacts), "by_type": by_type}


def run_smoke_benchmark(fn: Callable[[], Any], max_ms: float = 250.0) -> dict[str, float | bool]:
    start = perf_counter()
    _ = fn()
    elapsed_ms = (perf_counter() - start) * 1000.0
    return {"elapsed_ms": elapsed_ms, "within_budget": elapsed_ms <= max_ms}
