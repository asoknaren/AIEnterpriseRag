from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from strategies import (
    attach_metadata_envelope,
    build_raptor_hierarchy,
    contextual_chunk_artifacts,
    extract_factoids,
    generate_qa_pairs,
    generate_summaries_with_model,
    semantic_chunk_artifacts,
)


@dataclass
class StrategyStatus:
    name: str
    status: str
    error: str | None = None


class StrategyOrchestrator:
    def __init__(self, timeout_seconds: float = 5.0, retry_attempts: int = 1) -> None:
        self.timeout_seconds = timeout_seconds
        self.retry_attempts = max(1, retry_attempts)

    def _run_with_retry(self, fn: Callable[[], Any]) -> Any:
        last_error: Exception | None = None
        for _ in range(self.retry_attempts):
            try:
                return fn()
            except Exception as exc:  # pragma: no cover - explicit failure path exercised indirectly
                last_error = exc
        if last_error is None:
            raise RuntimeError("strategy failed without error")
        raise last_error

    def run_document(
        self,
        *,
        document_id: str,
        text: str,
        fail_strategies: set[str] | None = None,
        strategy_version: str = "3.0.0",
    ) -> dict[str, Any]:
        fail_strategies = fail_strategies or set()

        statuses: list[StrategyStatus] = []
        outputs: dict[str, Any] = {}

        semantic = self._execute_strategy(
            name="semantic_chunk",
            fail_strategies=fail_strategies,
            statuses=statuses,
            fn=lambda: semantic_chunk_artifacts(text, document_id=document_id),
        )
        if semantic is not None:
            outputs["semantic_chunk"] = attach_metadata_envelope(
                semantic,
                document_id=document_id,
                strategy="semantic_chunk",
                strategy_version=strategy_version,
            )

        contextual = self._execute_strategy(
            name="contextual_chunk",
            fail_strategies=fail_strategies,
            statuses=statuses,
            fn=lambda: contextual_chunk_artifacts(semantic or []),
        )
        if contextual is not None:
            outputs["contextual_chunk"] = attach_metadata_envelope(
                contextual,
                document_id=document_id,
                strategy="contextual_chunk",
                strategy_version=strategy_version,
            )

        summaries = self._execute_strategy(
            name="summary",
            fail_strategies=fail_strategies,
            statuses=statuses,
            fn=lambda: generate_summaries_with_model([item["chunk"] for item in semantic or []]),
        )
        if summaries is not None:
            outputs["summary"] = attach_metadata_envelope(
                summaries,
                document_id=document_id,
                strategy="summary",
                strategy_version=strategy_version,
            )

        raptor = self._execute_strategy(
            name="raptor",
            fail_strategies=fail_strategies,
            statuses=statuses,
            fn=lambda: build_raptor_hierarchy([item["chunk"] for item in semantic or []], document_id=document_id),
        )
        if raptor is not None:
            raptor_items = [raptor["root"], *raptor["children"]]
            outputs["raptor"] = attach_metadata_envelope(
                raptor_items,
                document_id=document_id,
                strategy="raptor",
                strategy_version=strategy_version,
            )

        qa_pairs = self._execute_strategy(
            name="qa_pairs",
            fail_strategies=fail_strategies,
            statuses=statuses,
            fn=lambda: generate_qa_pairs([item["chunk"] for item in semantic or []]),
        )
        if qa_pairs is not None:
            outputs["qa_pairs"] = attach_metadata_envelope(
                qa_pairs,
                document_id=document_id,
                strategy="qa_pairs",
                strategy_version=strategy_version,
            )

        factoids = self._execute_strategy(
            name="factoids",
            fail_strategies=fail_strategies,
            statuses=statuses,
            fn=lambda: extract_factoids([item["chunk"] for item in semantic or []]),
        )
        if factoids is not None:
            outputs["factoids"] = attach_metadata_envelope(
                factoids,
                document_id=document_id,
                strategy="factoids",
                strategy_version=strategy_version,
            )

        failures = [item for item in statuses if item.status == "failed"]
        run_status = "partial-failed" if failures else "completed"

        return {
            "run_id": f"run-{document_id}",
            "document_id": document_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "timeout_seconds": self.timeout_seconds,
            "retry_attempts": self.retry_attempts,
            "outputs": outputs,
            "strategy_statuses": [item.__dict__ for item in statuses],
            "run_status": run_status,
        }

    def _execute_strategy(
        self,
        *,
        name: str,
        fail_strategies: set[str],
        statuses: list[StrategyStatus],
        fn: Callable[[], Any],
    ) -> Any | None:
        if name in fail_strategies:
            statuses.append(StrategyStatus(name=name, status="failed", error="forced failure"))
            return None

        try:
            result = self._run_with_retry(fn)
            statuses.append(StrategyStatus(name=name, status="success"))
            return result
        except Exception as exc:  # pragma: no cover - exercised by failure path test
            statuses.append(StrategyStatus(name=name, status="failed", error=str(exc)))
            return None
