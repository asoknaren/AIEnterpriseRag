from dataclasses import dataclass
from typing import Any


@dataclass
class ArtifactContract:
    artifact_type: str
    document_id: str
    source_uri: str
    metadata: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "document_id": self.document_id,
            "source_uri": self.source_uri,
            "metadata": self.metadata,
        }
