from __future__ import annotations

from typing import Any


def plan_reprocessing(old_artifacts: list[dict[str, Any]], new_strategy_version: str) -> list[dict[str, Any]]:
    updates: list[dict[str, Any]] = []
    for item in old_artifacts:
        metadata = dict(item.get("metadata", {}))
        metadata["chunk_strategy_version"] = new_strategy_version
        updates.append({**item, "metadata": metadata})
    return updates


def detect_orphaned_records(existing_artifact_ids: set[str], submitted_artifacts: list[dict[str, Any]]) -> list[str]:
    submitted_ids = {item["artifact_id"] for item in submitted_artifacts}
    return sorted(existing_artifact_ids - submitted_ids)
