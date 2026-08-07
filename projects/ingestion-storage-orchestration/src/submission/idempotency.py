from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any


@dataclass
class SubmissionDecision:
    action: str
    idempotency_key: str


class IdempotencyRegistry:
    def __init__(self) -> None:
        self._active: dict[str, str] = {}

    def build_key(self, artifact: dict[str, Any]) -> str:
        checksum = sha256(artifact["content"].encode("utf-8")).hexdigest()
        return f"{artifact['document_id']}::{artifact['artifact_type']}::{checksum}"

    def decide(self, artifact: dict[str, Any]) -> SubmissionDecision:
        key = self.build_key(artifact)
        artifact_id = artifact["artifact_id"]

        if key not in self._active:
            self._active[key] = artifact_id
            return SubmissionDecision(action="create", idempotency_key=key)

        if self._active[key] == artifact_id:
            return SubmissionDecision(action="skip_duplicate", idempotency_key=key)

        self._active[key] = artifact_id
        return SubmissionDecision(action="update", idempotency_key=key)


def plan_submission_actions(artifacts: list[dict[str, Any]], registry: IdempotencyRegistry) -> list[SubmissionDecision]:
    return [registry.decide(artifact) for artifact in artifacts]
