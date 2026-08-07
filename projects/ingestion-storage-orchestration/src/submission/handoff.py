from __future__ import annotations

from typing import Any

from bridge.fastapi_payload_mapper import map_bundle_to_fastapi_payload
from submission.idempotency import IdempotencyRegistry, plan_submission_actions
from submission.payload_contract import batch_artifacts, validate_handoff_payload


class HandoffPlanner:
    def __init__(self, registry: IdempotencyRegistry | None = None) -> None:
        self.registry = registry or IdempotencyRegistry()

    def prepare(self, bundle: dict[str, Any], batch_size: int = 20) -> dict[str, Any]:
        payload = map_bundle_to_fastapi_payload(bundle)
        is_valid, errors = validate_handoff_payload(payload)
        if not is_valid:
            raise ValueError("; ".join(errors))

        actions = plan_submission_actions(payload["artifacts"], self.registry)
        batches = batch_artifacts(payload["artifacts"], batch_size=batch_size)
        return {
            "payload": payload,
            "actions": [item.__dict__ for item in actions],
            "batches": batches,
        }
