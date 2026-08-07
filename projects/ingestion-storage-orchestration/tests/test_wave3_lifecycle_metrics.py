from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from reliability.telemetry import RunTelemetryTracker


def test_lifecycle_transitions_for_success_and_partial_failure():
    tracker = RunTelemetryTracker()
    tracker.start("run-801", "doc-801")
    tracker.transition("run-801", "in-progress")
    tracker.transition("run-801", "completed")
    assert tracker.get("run-801").state == "completed"

    tracker.start("run-802", "doc-802")
    tracker.transition("run-802", "in-progress")
    tracker.transition("run-802", "partial-failed")
    assert tracker.get("run-802").state == "partial-failed"


def test_metrics_emission_contains_expected_counters_and_durations():
    tracker = RunTelemetryTracker()
    tracker.start("run-803", "doc-803")
    tracker.increment("run-803", accepted=10, rejected=2, retried=3, persisted=8)
    tracker.set_durations("run-803", parse_ms=11.0, validate_ms=22.0, submit_ms=33.0, total_ms=70.0)

    run = tracker.get("run-803")
    assert run.metrics.accepted == 10
    assert run.metrics.rejected == 2
    assert run.metrics.retried == 3
    assert run.metrics.persisted == 8
    assert run.metrics.parse_ms == 11.0
    assert run.metrics.validate_ms == 22.0
    assert run.metrics.submit_ms == 33.0
    assert run.metrics.total_ms == 70.0
