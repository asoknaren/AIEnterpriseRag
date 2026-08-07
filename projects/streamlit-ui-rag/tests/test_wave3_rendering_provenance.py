from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from rendering import build_related_artifact_links, render_provenance_view, render_ranked_results


def test_rendering_states_and_ranking_order():
    empty = render_ranked_results([])
    assert empty == []

    single = render_ranked_results([{"artifact_id": "a1", "score": 0.5, "artifact_type": "semantic_chunk", "document_id": "doc-a", "content": "alpha"}])
    assert len(single) == 1

    multi = render_ranked_results(
        [
            {"artifact_id": "a2", "score": 0.3, "artifact_type": "semantic_chunk", "document_id": "doc-b", "content": "beta"},
            {"artifact_id": "a3", "score": 0.9, "artifact_type": "contextual_chunk", "document_id": "doc-c", "content": "gamma"},
        ]
    )
    assert [item["artifact_id"] for item in multi] == ["a3", "a2"]


def test_provenance_completeness_and_related_drilldown_links():
    item = {
        "artifact_id": "a9",
        "metadata": {
            "chunk_strategy": "semantic_chunk",
            "chunk_strategy_version": "3.0.0",
            "source_uri": "https://example.com",
            "source_type": "pdf",
            "related_artifacts": ["a8", "a7"],
        },
        "lineage": {"source_ref": "p2:l9"},
    }

    provenance = render_provenance_view(item)
    assert provenance["strategy_type"] == "semantic_chunk"
    assert provenance["strategy_version"] == "3.0.0"
    assert provenance["source_uri"]
    assert provenance["section_marker"] == "p2:l9"

    links = build_related_artifact_links(item)
    assert [entry["artifact_id"] for entry in links] == ["a8", "a7"]
