from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256


@dataclass
class EmbeddingMetadata:
    model_provider: str
    model_name: str


class DeterministicEmbeddingProvider:
    def __init__(self, model_provider: str = "mock", model_name: str = "mock-embedding-v1") -> None:
        self.meta = EmbeddingMetadata(model_provider=model_provider, model_name=model_name)

    def embed_text(self, text: str) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()
        # Stable 8-dim pseudo-embedding in range [0, 1].
        return [byte / 255.0 for byte in digest[:8]]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]
