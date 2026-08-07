from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from strategies import (
    attach_metadata_envelope,
    build_raptor_hierarchy,
    contextual_chunk_artifacts,
    extract_factoids,
    generate_qa_pairs,
    generate_summaries_with_model,
    semantic_chunk_artifacts,
)


def test_semantic_and_contextual_artifacts_include_expected_fields():
    text = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda"
    semantic = semantic_chunk_artifacts(text, document_id="doc-200", max_chars=25, overlap=5)
    contextual = contextual_chunk_artifacts(semantic, headers=["H1", "H2", "H3"]) 

    assert semantic
    assert all(item["token_count"] >= 1 for item in semantic)
    assert contextual
    assert all(item["context"] for item in contextual)
    assert all("source_span" in item for item in contextual)


def test_raptor_hierarchy_integrity_has_valid_parent_links():
    chunks = ["Chunk one content", "Chunk two content", "Chunk three content"]
    graph = build_raptor_hierarchy(chunks, document_id="doc-201")

    root_id = graph["root"]["node_id"]
    assert graph["root"]["parent_node_id"] is None
    assert all(child["parent_node_id"] == root_id for child in graph["children"])


def test_summary_length_policy_and_model_metadata():
    chunks = ["Summary candidate one", "Summary candidate two"]
    summaries = generate_summaries_with_model(chunks, min_chars=12, max_chars=20)

    assert summaries
    assert all(12 <= item["summary_length"] <= 20 for item in summaries)
    assert all(item["model_provider"] == "ollama" for item in summaries)


def test_qa_provenance_and_factoid_deduplication():
    chunks = ["Paris is capital of France", "Paris has landmarks", "Berlin is capital of Germany"]
    qa_pairs = generate_qa_pairs(chunks, source_ref_prefix="sec")
    factoids = extract_factoids(chunks)

    assert all(item["source_spans"][0]["source_ref"].startswith("sec:") for item in qa_pairs)
    canonical_values = [item["canonical_value"] for item in factoids]
    assert canonical_values.count("paris") == 1


def test_metadata_envelope_attaches_strategy_and_model_fields():
    semantic = semantic_chunk_artifacts("Alpha beta gamma", document_id="doc-202")
    envelope = attach_metadata_envelope(semantic, document_id="doc-202", strategy="semantic_chunk", strategy_version="2.0.0")

    assert envelope
    assert all(item["metadata"]["chunk_strategy"] == "semantic_chunk" for item in envelope)
    assert all(item["metadata"]["chunk_strategy_version"] == "2.0.0" for item in envelope)
