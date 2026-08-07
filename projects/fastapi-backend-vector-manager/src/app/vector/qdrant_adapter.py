from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any


@dataclass
class VectorPoint:
    point_id: str
    embedding: list[float]
    payload: dict[str, Any]


class InMemoryQdrantAdapter:
    def __init__(self) -> None:
        self._points: dict[str, VectorPoint] = {}

    def initialize_collection(self, name: str) -> dict[str, str]:
        return {"collection": name, "status": "ready"}

    def upsert(self, point_id: str, embedding: list[float], payload: dict[str, Any]) -> None:
        self._points[point_id] = VectorPoint(point_id=point_id, embedding=embedding, payload=payload)

    def delete(self, point_id: str) -> None:
        self._points.pop(point_id, None)

    def update(self, point_id: str, embedding: list[float], payload: dict[str, Any]) -> None:
        self.upsert(point_id, embedding, payload)

    def search(self, query_embedding: list[float], top_k: int = 5, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        filters = filters or {}
        scored: list[dict[str, Any]] = []
        for point in self._points.values():
            if not _payload_matches(point.payload, filters):
                continue
            score = _cosine_similarity(query_embedding, point.embedding)
            scored.append({"point_id": point.point_id, "score": score, "payload": point.payload})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]


def _payload_matches(payload: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, value in filters.items():
        if payload.get(key) != value:
            return False
    return True


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
