from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass


@dataclass
class InMemoryStore:
    documents: dict[str, dict]
    artifacts: dict[str, dict]


class InMemoryDatabase:
    def __init__(self) -> None:
        self._documents: dict[str, dict] = {}
        self._artifacts: dict[str, dict] = {}

    @property
    def documents(self) -> dict[str, dict]:
        return self._documents

    @property
    def artifacts(self) -> dict[str, dict]:
        return self._artifacts

    def snapshot(self) -> InMemoryStore:
        return InMemoryStore(documents=deepcopy(self._documents), artifacts=deepcopy(self._artifacts))

    def restore(self, snapshot: InMemoryStore) -> None:
        self._documents = snapshot.documents
        self._artifacts = snapshot.artifacts
