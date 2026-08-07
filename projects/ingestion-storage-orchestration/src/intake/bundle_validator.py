from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from intake.bundle_parser import parse_bundle


def validate_bundle(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    try:
        parse_bundle(payload)
        return True, []
    except ValidationError as exc:
        errors = []
        for item in exc.errors():
            loc = ".".join(str(part) for part in item.get("loc", []))
            msg = item.get("msg", "validation error")
            errors.append(f"{loc}: {msg}")
        return False, errors
