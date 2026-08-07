from __future__ import annotations

from typing import Any

from state.run_state_store import InMemoryRunStateStore


class ForcedInterruption(RuntimeError):
    pass


def execute_with_recovery(
    run_id: str,
    document_id: str,
    artifacts: list[dict[str, Any]],
    fail_after: int | None = None,
) -> dict[str, Any]:
    store = InMemoryRunStateStore()
    store.create(run_id=run_id, document_id=document_id)

    processed: list[str] = []
    for index, artifact in enumerate(artifacts):
        if fail_after is not None and index >= fail_after:
            store.update_status(run_id, "interrupted")
            raise ForcedInterruption("forced mid-run interruption")
        processed.append(artifact["artifact_id"])

    store.update_status(run_id, "completed")
    return {"processed": processed, "state": store.get(run_id)}
