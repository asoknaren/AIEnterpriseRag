from __future__ import annotations

from typing import Any

REQUIRED_ARTIFACT_FIELDS = {
    "artifact_id",
    "document_id",
    "artifact_type",
    "content",
    "metadata",
    "lineage",
}

MAX_BATCH_SIZE = 50
MIN_BATCH_SIZE = 1
MAX_CONTENT_CHARS = 20000


def validate_handoff_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    artifacts = payload.get("artifacts", [])

    if not isinstance(artifacts, list):
        return False, ["artifacts must be a list"]

    if len(artifacts) < MIN_BATCH_SIZE or len(artifacts) > MAX_BATCH_SIZE:
        errors.append(f"artifacts batch size must be between {MIN_BATCH_SIZE} and {MAX_BATCH_SIZE}")

    for index, artifact in enumerate(artifacts):
        missing = sorted(REQUIRED_ARTIFACT_FIELDS - set(artifact.keys()))
        if missing:
            errors.append(f"artifacts.{index} missing fields: {', '.join(missing)}")
            continue

        if "embedding" in artifact:
            errors.append(f"artifacts.{index} must not include embedding")

        content = artifact.get("content", "")
        if not isinstance(content, str) or not content.strip():
            errors.append(f"artifacts.{index}.content must be non-empty string")
        elif len(content) > MAX_CONTENT_CHARS:
            errors.append(f"artifacts.{index}.content exceeds max size")

        metadata = artifact.get("metadata", {})
        for field in ("source_uri", "source_type", "chunk_strategy", "chunk_strategy_version"):
            if field not in metadata:
                errors.append(f"artifacts.{index}.metadata missing {field}")

        lineage = artifact.get("lineage", {})
        if "source_ref" not in lineage:
            errors.append(f"artifacts.{index}.lineage missing source_ref")

    return len(errors) == 0, errors


def batch_artifacts(artifacts: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    if batch_size < MIN_BATCH_SIZE or batch_size > MAX_BATCH_SIZE:
        raise ValueError("batch_size outside allowed bounds")
    return [artifacts[index : index + batch_size] for index in range(0, len(artifacts), batch_size)]
