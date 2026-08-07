from __future__ import annotations

from typing import Any


def render_ranked_results(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = sorted(items, key=lambda item: item.get("score", 0.0), reverse=True)
    rendered: list[dict[str, Any]] = []
    for item in ranked:
        content = item.get("content", "")
        rendered.append(
            {
                "artifact_id": item.get("artifact_id"),
                "score": item.get("score", 0.0),
                "artifact_type": item.get("artifact_type"),
                "source_identifier": item.get("document_id"),
                "preview": content[:140],
                "context_size": len(content),
                "content": content,
                "metadata": item.get("metadata", {}),
                "lineage": item.get("lineage", {}),
            }
        )
    return rendered


def render_provenance_view(item: dict[str, Any]) -> dict[str, Any]:
    metadata = item.get("metadata", {})
    lineage = item.get("lineage", {})
    return {
        "strategy_type": metadata.get("chunk_strategy"),
        "strategy_version": metadata.get("chunk_strategy_version"),
        "source_uri": metadata.get("source_uri"),
        "source_type": metadata.get("source_type"),
        "section_marker": lineage.get("source_ref"),
    }


def build_related_artifact_links(item: dict[str, Any]) -> list[dict[str, str]]:
    related = item.get("metadata", {}).get("related_artifacts", [])
    return [{"artifact_id": rid, "label": f"Related {rid}"} for rid in related]
