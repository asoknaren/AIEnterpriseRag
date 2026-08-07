from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from orchestrator import StrategyOrchestrator
from quality import evaluate_metadata_completeness, regression_snapshot, run_smoke_benchmark


def _artifacts() -> list[dict]:
    run = StrategyOrchestrator(timeout_seconds=2.0, retry_attempts=2).run_document(
        document_id="doc-q4",
        text="alpha beta gamma delta epsilon zeta eta theta iota kappa lambda",
        strategy_version="4.0.0",
    )
    artifacts = []
    for items in run["outputs"].values():
        artifacts.extend(items)
    return artifacts


def test_regression_suite_with_baseline_snapshot():
    artifacts = _artifacts()
    snapshot = regression_snapshot(artifacts)

    assert snapshot["artifact_count"] >= 6
    assert "semantic_chunk" in snapshot["by_type"]


def test_metadata_completeness_is_full_required_coverage():
    report = evaluate_metadata_completeness(_artifacts())

    assert report.metadata_completeness == 1.0
    assert report.missing_fields == []


def test_smoke_benchmark_within_processing_budget():
    result = run_smoke_benchmark(_artifacts, max_ms=600.0)
    assert result["within_budget"] is True
