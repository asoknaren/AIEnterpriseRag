# Project 3 Implementation Plan: FastAPI Platform Service

## Objective
Build the central FastAPI platform service that exposes CRUD and retrieval APIs, owns embedding generation and vectorization, supports configuration-driven PostgreSQL and Qdrant modes, and provides stable integration contracts for ingestion and search clients.

## Scope
- In scope: API contracts, embedding and vectorization pipeline, storage adapters, mode configuration, lifecycle operations, retrieval endpoints, and operational endpoints.
- Out of scope: chunk generation logic and UI rendering.

## Milestone 1: Service Skeleton and Configuration

### Task 1.1 Create API skeleton and contract baseline
Subtasks:
1. Initialize FastAPI app structure with versioned routes.
2. Define core request and response models.
3. Add common error envelope and trace identifiers.

Checkpoint tests:
1. Route discovery test verifying all baseline endpoints are registered.
2. Model validation test for required fields and error handling behavior.

Pass criteria:
1. Baseline routes resolve successfully.
2. Invalid request bodies return consistent validation responses.

### Task 1.2 Implement configuration-driven storage mode selection
Subtasks:
1. Add configuration profiles for PostgreSQL-only, Qdrant-only, and combined mode.
2. Implement adapter selection at service startup.
3. Expose active mode through operational endpoint.

Checkpoint tests:
1. Startup mode test for each profile.
2. Operational status test returning active backend mode.

Pass criteria:
1. Service starts successfully in all three modes.
2. Active mode is accurately reported and logged.

## Milestone 2: CRUD and Metadata Lifecycle

### Task 2.1 Implement document and artifact CRUD
Subtasks:
1. Implement create and read operations.
2. Implement update operations with optimistic version checks.
3. Implement delete operations with cascading artifact behavior.

Checkpoint tests:
1. CRUD contract test for create, read, update, and delete paths.
2. Version conflict test for stale update requests.

Pass criteria:
1. CRUD operations satisfy contract responses across configured modes.
2. Version conflicts are detected and handled with explicit error codes.

### Task 2.2 Implement metadata persistence adapter for PostgreSQL
Subtasks:
1. Implement relational writes for documents and artifacts.
2. Implement status and audit metadata persistence.
3. Add transactional boundaries for multi-record operations.

Checkpoint tests:
1. Transaction integrity test with forced mid-transaction error.
2. Read-after-write consistency test for metadata retrieval.

Pass criteria:
1. Failed transactions rollback cleanly.
2. Metadata retrieval reflects committed writes accurately.

## Milestone 3: Embedding Pipeline, Vector Retrieval, and Search APIs

### Task 3.1 Implement embedding generation pipeline
Subtasks:
1. Implement provider-agnostic embedding adapter inside FastAPI.
2. Add batching, rate-limit handling, and retry policy for embedding calls.
3. Persist embedding model metadata alongside generated vectors.

Checkpoint tests:
1. Embedding contract test with mock provider and one real provider profile.
2. Determinism test for unchanged input, ensuring stable vector count and mapping.

Pass criteria:
1. FastAPI can generate embeddings from ingestion payload text without Project 2 embedding input.
2. Embedding metadata is captured and queryable per artifact.

### Task 3.2 Implement Qdrant adapter and vector upsert path
Subtasks:
1. Add vector collection initialization logic.
2. Implement upsert for FastAPI-generated vectors and payload metadata.
3. Implement delete and update operations for vector records.

Checkpoint tests:
1. Vector upsert test with known embeddings and payload attributes.
2. Vector delete test ensuring removed points are not returned in search.

Pass criteria:
1. Upsert and delete behavior is correct in repeated runs.
2. Payload metadata is queryable for filter scenarios.

### Task 3.3 Implement retrieval endpoints
Subtasks:
1. Implement vector similarity search endpoint.
2. Implement metadata-filtered retrieval endpoint.
3. Implement source-context enrichment in response payload.

Checkpoint tests:
1. Relevance smoke test with seeded fixture vectors and expected top-k membership.
2. Filter correctness test with strategy and source metadata predicates.

Pass criteria:
1. Top-k results include expected seeded neighbors.
2. Filters constrain results correctly without leakage.

## Milestone 4: Operations, Security Baseline, and Release

### Task 4.1 Implement operational endpoints and telemetry hooks
Subtasks:
1. Add health and readiness endpoints.
2. Add ingestion status lookup endpoints.
3. Add request metrics and structured logging hooks.

Checkpoint tests:
1. Health endpoint test for service and backend dependencies.
2. Telemetry smoke test verifying logs and key metrics are emitted.

Pass criteria:
1. Health and readiness are accurate under normal and degraded conditions.
2. Telemetry contains trace id, endpoint, latency, and outcome fields.

### Task 4.2 Release candidate checkpoint
Subtasks:
1. Publish API usage guide for Project 2 and Project 4.
2. Freeze API version for first integration release.
3. Execute interoperability suite with Project 2 ingestion and Project 4 search.

Checkpoint tests:
1. End-to-end API interoperability test across create, search, update, and delete.
2. Mode parity test across PostgreSQL-only, Qdrant-only, and combined mode.

Pass criteria:
1. Interoperability suite is green.
2. Mode parity matrix passes supported feature expectations.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. API contracts are stable and consumable by ingestion and search projects.
3. Service supports the required backend modes with verifiable behavior.