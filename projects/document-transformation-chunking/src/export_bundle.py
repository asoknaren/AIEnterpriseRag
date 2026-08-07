from __future__ import annotations

from hashlib import sha256
from typing import Any


def _artifact_checksum(artifact: dict[str, Any]) -> str:
    canonical = "|".join(
        [
            artifact.get("artifact_id", ""),
            artifact.get("artifact_type", ""),
            artifact.get("content", ""),
            artifact.get("metadata", {}).get("chunk_strategy", ""),
            artifact.get("metadata", {}).get("chunk_strategy_version", ""),
            artifact.get("lineage", {}).get("source_ref", ""),
        ]
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def build_ingestion_bundle(orchestrator_run: dict[str, Any]) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []
    manifests: list[dict[str, str]] = []

    for strategy_name in sorted(orchestrator_run["outputs"].keys()):
        for artifact in orchestrator_run["outputs"][strategy_name]:
            checksum = _artifact_checksum(artifact)
            artifact_payload = {
                "artifact_id": artifact["artifact_id"],
                "document_id": artifact["document_id"],
                "artifact_type": artifact["artifact_type"],
                "content": artifact["content"],
                "metadata": artifact["metadata"],
                "lineage": artifact["lineage"],
                "checksum": checksum,
            }
            artifacts.append(artifact_payload)
            manifests.append({"artifact_id": artifact["artifact_id"], "checksum": checksum})

    return {
        "run_id": orchestrator_run["run_id"],
        "document_id": orchestrator_run["document_id"],
        "run_status": orchestrator_run["run_status"],
        "artifacts": artifacts,
        "manifests": manifests,
    }
