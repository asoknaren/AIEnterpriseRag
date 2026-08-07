from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from reliability.ingestion_executor import IngestionExecutor
from reliability.retry_policy import RetryPolicy


class RetryableServerError(Exception):
    pass


class ValidationFailure(Exception):
    pass


def test_retry_behavior_recovers_within_budget():
    calls = {"count": 0}

    def submit():
        calls["count"] += 1
        if calls["count"] < 3:
            raise RetryableServerError("transient 5xx")
        return {"ok": True}

    executor = IngestionExecutor(retry_policy=RetryPolicy(max_retries=4))
    result = executor.submit_with_retry(
        run_id="run-701",
        document_id="doc-701",
        artifact={"artifact_id": "a-701"},
        submit_fn=submit,
        is_retryable=lambda exc: isinstance(exc, RetryableServerError),
    )

    assert result["status"] == "success"
    assert result["attempts"] == 3


def test_dead_letter_routing_for_non_retryable_failures():
    def submit():
        raise ValidationFailure("hard validation failure")

    executor = IngestionExecutor(retry_policy=RetryPolicy(max_retries=3))
    result = executor.submit_with_retry(
        run_id="run-702",
        document_id="doc-702",
        artifact={"artifact_id": "a-702", "content": "x"},
        submit_fn=submit,
        is_retryable=lambda exc: isinstance(exc, RetryableServerError),
    )

    assert result["status"] == "non-retryable"
    assert len(executor.dead_letter.records) == 1
    assert executor.dead_letter.records[0].artifact_id == "a-702"
