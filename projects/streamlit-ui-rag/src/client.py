from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class ClientTimeoutError(RuntimeError):
    pass


@dataclass
class ClientConfig:
    timeout_seconds: float = 2.0
    max_retries: int = 2


class FastApiSearchClient:
    def __init__(self, transport: Callable[[dict[str, Any]], dict[str, Any]], config: ClientConfig | None = None) -> None:
        self.transport = transport
        self.config = config or ClientConfig()

    def search(self, payload: dict[str, Any]) -> dict[str, Any]:
        attempts = 0
        last_error: Exception | None = None
        while attempts < self.config.max_retries:
            attempts += 1
            try:
                response = self.transport(payload)
                return self._parse_response(response)
            except ClientTimeoutError as exc:
                last_error = exc
            except Exception as exc:
                last_error = exc
                break

        if isinstance(last_error, ClientTimeoutError):
            raise ClientTimeoutError("request timed out after retries")
        raise RuntimeError(f"request failed: {last_error}")

    def _parse_response(self, response: dict[str, Any]) -> dict[str, Any]:
        items = response.get("items", [])
        parsed = []
        for item in items:
            parsed.append(
                {
                    "artifact_id": item.get("artifact_id"),
                    "score": float(item.get("score", 0.0)),
                    "artifact_type": item.get("artifact_type"),
                    "document_id": item.get("document_id"),
                    "content": item.get("content", ""),
                    "metadata": item.get("metadata", {}),
                    "lineage": item.get("lineage", {}),
                }
            )
        return {"items": parsed}
