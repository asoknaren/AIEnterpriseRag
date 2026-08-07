from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.routes_artifacts import router as artifacts_router
from app.api.v1.routes_documents import router as documents_router
from app.api.v1.routes_embedding import router as embedding_router
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_ingestion import router as ingestion_router
from app.api.v1.routes_ops import router as ops_router
from app.api.v1.routes_search import router as search_router
from app.config.settings import AppSettings
from app.embedding.provider import DeterministicEmbeddingProvider
from app.models.errors import ErrorEnvelope
from app.runtime.mode_selector import select_adapters
from app.storage.in_memory_db import InMemoryDatabase
from app.storage.repository import Repository
from app.telemetry.hooks import InMemoryTelemetry, install_telemetry_middleware
from app.vector.qdrant_adapter import InMemoryQdrantAdapter


def create_app() -> FastAPI:
    settings = AppSettings.from_env()

    app = FastAPI(title="FastAPI Backend Vector Manager", version="0.1.0")
    app.state.active_mode = settings.profile
    app.state.adapters = select_adapters(settings.profile)
    app.state.db = InMemoryDatabase()
    app.state.repository = Repository(app.state.db)
    app.state.embedding_provider = DeterministicEmbeddingProvider()
    app.state.vector_adapter = InMemoryQdrantAdapter()
    app.state.ingestion_status = {}
    app.state.telemetry = InMemoryTelemetry()
    app.state.vector_adapter.initialize_collection("artifacts")

    install_telemetry_middleware(app, app.state.telemetry)

    app.include_router(documents_router)
    app.include_router(artifacts_router)
    app.include_router(embedding_router)
    app.include_router(search_router)
    app.include_router(ops_router)
    app.include_router(health_router)
    app.include_router(ingestion_router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        trace_id = str(uuid4())
        envelope = ErrorEnvelope(
            trace_id=trace_id,
            error_code="request_validation_error",
            message="Request body validation failed",
            details=exc.errors(),
        )
        return JSONResponse(status_code=422, content=envelope.model_dump())

    return app


app = create_app()
