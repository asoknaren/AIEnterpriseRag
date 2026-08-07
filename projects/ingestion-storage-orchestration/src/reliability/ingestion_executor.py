from __future__ import annotations

from typing import Any, Callable

from reliability.retry_policy import DeadLetterQueue, RetryPolicy
from reliability.telemetry import RunTelemetryTracker


class IngestionExecutor:
    def __init__(
        self,
        retry_policy: RetryPolicy | None = None,
        telemetry: RunTelemetryTracker | None = None,
        dead_letter: DeadLetterQueue | None = None,
    ) -> None:
        self.retry_policy = retry_policy or RetryPolicy()
        self.telemetry = telemetry or RunTelemetryTracker()
        self.dead_letter = dead_letter or DeadLetterQueue()

    def submit_with_retry(
        self,
        *,
        run_id: str,
        document_id: str,
        artifact: dict[str, Any],
        submit_fn: Callable[[], Any],
        is_retryable: Callable[[Exception], bool],
    ) -> dict[str, Any]:
        if run_id not in self.telemetry._runs:
            self.telemetry.start(run_id=run_id, document_id=document_id)
        self.telemetry.transition(run_id, "in-progress")

        result = self.retry_policy.execute(submit_fn, is_retryable=is_retryable)
        self.telemetry.increment(run_id, accepted=1)

        if result.status == "success":
            if result.attempts > 1:
                self.telemetry.increment(run_id, retried=result.attempts - 1)
            self.telemetry.increment(run_id, persisted=1)
            self.telemetry.transition(run_id, "completed")
            return {"status": "success", "attempts": result.attempts, "value": result.value}

        if result.status == "retry-exhausted":
            self.dead_letter.push(artifact_id=artifact["artifact_id"], reason=result.error or "retry exhausted", payload=artifact)
            self.telemetry.increment(run_id, retried=max(0, result.attempts - 1), rejected=1)
            self.telemetry.transition(run_id, "partial-failed")
            return {"status": "retry-exhausted", "attempts": result.attempts}

        self.dead_letter.push(artifact_id=artifact["artifact_id"], reason=result.error or "non-retryable", payload=artifact)
        self.telemetry.increment(run_id, rejected=1)
        self.telemetry.transition(run_id, "failed")
        return {"status": "non-retryable", "attempts": result.attempts}
