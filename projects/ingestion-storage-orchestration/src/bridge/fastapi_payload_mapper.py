from __future__ import annotations

from typing import Any

from bridge.ordering import deterministic_order


REQUIRED_METADATA_FIELDS = {
    "source_uri",
    "source_type",
    "chunk_strategy",
    "chunk_strategy_version",
}


def map_bundle_to_fastapi_payload(bundle: dict[str, Any]) -> dict[str, Any]:
    mapped_artifacts = []
    for artifact in bundle["artifacts"]:
        mapped_artifacts.append(
            {
                "artifact_id": artifact["artifact_id"],
                "document_id": artifact["document_id"],
                "artifact_type": artifact["artifact_type"],
                "content": artifact["content"],
                "metadata": artifact.get("metadata", {}),
                "lineage": artifact.get("lineage", {}),
            }
        )

    return {
        "run_id": bundle["run_id"],
        "document_id": bundle["document_id"],
        "artifacts": deterministic_order(mapped_artifacts),
    }
