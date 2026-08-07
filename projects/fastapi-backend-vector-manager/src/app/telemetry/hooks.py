from __future__ import annotations

from time import perf_counter
from typing import Callable
from uuid import uuid4

from fastapi import Request, Response


class InMemoryTelemetry:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def emit(self, event: dict) -> None:
        self.events.append(event)


def install_telemetry_middleware(app, telemetry: InMemoryTelemetry) -> None:
    @app.middleware("http")
    async def telemetry_middleware(request: Request, call_next: Callable):
        trace_id = str(uuid4())
        start = perf_counter()
        response: Response = await call_next(request)
        elapsed_ms = (perf_counter() - start) * 1000.0
        telemetry.emit(
            {
                "trace_id": trace_id,
                "endpoint": request.url.path,
                "method": request.method,
                "latency_ms": elapsed_ms,
                "outcome": "ok" if response.status_code < 500 else "error",
                "status_code": response.status_code,
            }
        )
        response.headers["x-trace-id"] = trace_id
        return response
