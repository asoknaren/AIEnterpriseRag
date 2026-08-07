from __future__ import annotations

from typing import Any

from artifact_schema import REQUIRED_EXTENSION_FIELDS


def required_extension_fields(artifact_type: str) -> set[str]:
    return REQUIRED_EXTENSION_FIELDS.get(artifact_type, set())


def has_required_extension_fields(artifact_type: str, extension: dict[str, Any]) -> tuple[bool, list[str]]:
    required = required_extension_fields(artifact_type)
    missing = sorted(field for field in required if field not in extension)
    return len(missing) == 0, missing
