from __future__ import annotations

from typing import Any

from export_bundle import build_ingestion_bundle
from orchestrator import StrategyOrchestrator
from versioning import STRATEGY_VERSIONS


def build_handoff_package(document_id: str, text: str) -> dict[str, Any]:
    orchestrator = StrategyOrchestrator(timeout_seconds=2.0, retry_attempts=2)
    run = orchestrator.run_document(
        document_id=document_id,
        text=text,
        strategy_version=STRATEGY_VERSIONS["semantic_chunk"],
    )
    bundle = build_ingestion_bundle(run)
    return {
        "interface_version": "4.0.0",
        "strategy_versions": STRATEGY_VERSIONS,
        "bundle": bundle,
    }
