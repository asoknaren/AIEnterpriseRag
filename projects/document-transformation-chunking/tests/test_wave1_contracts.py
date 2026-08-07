from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from contracts import ArtifactContract


def test_artifact_contract_payload_contains_required_fields():
    contract = ArtifactContract(
        artifact_type="semantic_chunk",
        document_id="doc-001",
        source_uri="https://example.com/doc.pdf",
        metadata={"strategy": "semantic", "version": "v1"},
    )

    payload = contract.to_payload()

    assert payload["artifact_type"] == "semantic_chunk"
    assert payload["document_id"] == "doc-001"
    assert payload["source_uri"] == "https://example.com/doc.pdf"
    assert payload["metadata"]["strategy"] == "semantic"
