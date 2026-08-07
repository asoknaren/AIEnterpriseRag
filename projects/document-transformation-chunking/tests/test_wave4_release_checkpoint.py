from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from config_profiles import ALTERNATE_PROFILE, DEFAULT_PROFILE, validate_profile
from handoff_package import build_handoff_package

REPO_ROOT = ROOT.parents[1]
PROJECT2_SRC = REPO_ROOT / "projects" / "ingestion-storage-orchestration" / "src"
sys.path.insert(0, str(PROJECT2_SRC.resolve()))

from submission.payload_contract import validate_handoff_payload


def test_handoff_package_accepted_by_project2_validator():
    package = build_handoff_package("doc-h1", "alpha beta gamma delta epsilon zeta")
    bundle = package["bundle"]

    payload = {
        "run_id": bundle["run_id"],
        "document_id": bundle["document_id"],
        "artifacts": [
            {
                "artifact_id": item["artifact_id"],
                "document_id": item["document_id"],
                "artifact_type": item["artifact_type"],
                "content": item["content"],
                "metadata": item["metadata"],
                "lineage": item["lineage"],
            }
            for item in bundle["artifacts"]
        ],
    }

    is_valid, errors = validate_handoff_payload(payload)
    assert is_valid, errors


def test_configuration_profiles_are_sane_in_default_and_alternate():
    assert validate_profile(DEFAULT_PROFILE)
    assert validate_profile(ALTERNATE_PROFILE)
