from __future__ import annotations

from bridge.fastapi_payload_mapper import REQUIRED_METADATA_FIELDS


def missing_required_metadata_fields(metadata: dict) -> list[str]:
    return sorted(field for field in REQUIRED_METADATA_FIELDS if field not in metadata)
