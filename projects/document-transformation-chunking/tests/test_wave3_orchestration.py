from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from orchestrator import StrategyOrchestrator


def test_orchestration_produces_all_six_strategy_outputs():
    orchestrator = StrategyOrchestrator(timeout_seconds=2.0, retry_attempts=2)
    text = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu"

    run = orchestrator.run_document(document_id="doc-401", text=text)

    assert run["run_status"] == "completed"
    assert set(run["outputs"].keys()) == {
        "semantic_chunk",
        "contextual_chunk",
        "summary",
        "raptor",
        "qa_pairs",
        "factoids",
    }


def test_failure_isolation_keeps_successful_strategy_outputs():
    orchestrator = StrategyOrchestrator(timeout_seconds=2.0, retry_attempts=2)
    text = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu"

    run = orchestrator.run_document(document_id="doc-402", text=text, fail_strategies={"qa_pairs"})

    assert run["run_status"] == "partial-failed"
    assert "qa_pairs" not in run["outputs"]
    assert "semantic_chunk" in run["outputs"]
    assert any(item["name"] == "qa_pairs" and item["status"] == "failed" for item in run["strategy_statuses"])
