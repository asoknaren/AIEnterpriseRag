from __future__ import annotations

import json
from typing import Any

from intake.bundle_models import IngestBundle


def parse_bundle(payload: str | dict[str, Any]) -> IngestBundle:
    data = json.loads(payload) if isinstance(payload, str) else payload
    return IngestBundle.model_validate(data)
