from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from strategies import (
    build_contextual_chunks,
    build_summary_artifacts,
    chunk_text_semantically,
)


def test_semantic_chunking_respects_target_size():
    text = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega."

    chunks = chunk_text_semantically(text, max_chars=40, overlap=10)

    assert len(chunks) >= 2
    assert all(len(chunk) <= 40 for chunk in chunks)


def test_contextual_chunking_includes_neighbor_context():
    chunks = ["Section one text", "Section two text"]
    contextual = build_contextual_chunks(chunks, headers=["Section one", "Section two"])

    assert contextual[0]["context"]
    assert contextual[0]["header"] == "Section one"
    assert contextual[1]["header"] == "Section two"


def test_summary_artifacts_are_bounded():
    chunks = ["A long chunk for summary generation", "Another chunk for summary generation"]
    summaries = build_summary_artifacts(chunks, max_chars=30)

    assert len(summaries) == 2
    assert all(len(item["summary"]) <= 30 for item in summaries)
