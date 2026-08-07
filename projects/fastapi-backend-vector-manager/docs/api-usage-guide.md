# API Usage Guide (Wave 4 RC)

## Base Endpoints
- Documents: /api/v1/documents
- Artifacts: /api/v1/artifacts
- Embeddings: /api/v1/embeddings/upsert
- Search: /api/v1/search/similarity and /api/v1/search/filter
- Operations: /api/v1/ops/mode
- Health/Readiness: /api/v1/health and /api/v1/readiness
- Ingestion Status: /api/v1/ingestion/status/{run_id}

## Integration Notes
- Project 2 should submit documents and embeddings in deterministic order.
- Project 4 should call similarity endpoint with filters for artifact_type/source_type.

## Version Freeze
- API integration release version: 4.0.0
