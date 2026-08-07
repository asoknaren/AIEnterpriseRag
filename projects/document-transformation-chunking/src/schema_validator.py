from __future__ import annotations

from typing import Any

from artifact_schema import validate_payload


def validate_artifact_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    is_valid, errors = validate_payload(payload)
    if is_valid:
        return True, []

    messages: list[str] = []
    for item in errors:
        loc = ".".join(str(part) for part in item.get("loc", []))
        msg = item.get("msg", "validation error")
        messages.append(f"{loc}: {msg}")
    return False, messages
