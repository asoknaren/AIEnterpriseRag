from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class RetryResult:
    status: str
    attempts: int
    value: Any | None = None
    error: str | None = None


@dataclass
class DeadLetterRecord:
    artifact_id: str
    reason: str
    payload: dict[str, Any]


class DeadLetterQueue:
    def __init__(self) -> None:
        self.records: list[DeadLetterRecord] = []

    def push(self, artifact_id: str, reason: str, payload: dict[str, Any]) -> None:
        self.records.append(DeadLetterRecord(artifact_id=artifact_id, reason=reason, payload=payload))


class RetryPolicy:
    def __init__(self, max_retries: int = 3) -> None:
        self.max_retries = max(1, max_retries)

    def execute(self, operation: Callable[[], Any], *, is_retryable: Callable[[Exception], bool]) -> RetryResult:
        attempts = 0
        while attempts < self.max_retries:
            attempts += 1
            try:
                value = operation()
                return RetryResult(status="success", attempts=attempts, value=value)
            except Exception as exc:
                if not is_retryable(exc):
                    return RetryResult(status="non-retryable", attempts=attempts, error=str(exc))
                if attempts >= self.max_retries:
                    return RetryResult(status="retry-exhausted", attempts=attempts, error=str(exc))
        return RetryResult(status="retry-exhausted", attempts=attempts, error="retry budget exhausted")
