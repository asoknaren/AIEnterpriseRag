from __future__ import annotations

from typing import Any


def deterministic_order(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        artifacts,
        key=lambda item: (
            item.get("artifact_type", ""),
            item.get("artifact_id", ""),
            item.get("document_id", ""),
        ),
    )
