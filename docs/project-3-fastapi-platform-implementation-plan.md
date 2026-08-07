# FastAPI Backend Vector Manager (Project 3) Implementation Plan

## Objective
Build the central FastAPI platform service that exposes CRUD and retrieval APIs, owns embedding generation and vectorization, supports configuration-driven PostgreSQL and Qdrant modes, and provides stable integration contracts for ingestion and search clients.

## Scope
- In scope: API contracts, embedding and vectorization pipeline, storage adapters, mode configuration, lifecycle operations, retrieval endpoints, and operational endpoints.
- Out of scope: chunk generation logic and UI rendering.

## Milestone 1: Service Skeleton and Configuration

### Task 1.1 Create API skeleton and contract baseline
- [x] Initialize FastAPI app structure with versioned routes.
- [x] Define core request and response models.
- [x] Add common error envelope and trace identifiers.

#### Checkpoint tests
- [x] Route discovery test verifying all baseline endpoints are registered.
- [x] Model validation test for required fields and error handling behavior.

#### Pass criteria
- [x] Baseline routes resolve successfully.
- [x] Invalid request bodies return consistent validation responses.

### Task 1.2 Implement configuration-driven storage mode selection
- [x] Add configuration profiles for PostgreSQL-only, Qdrant-only, and combined mode.
- [x] Implement adapter selection at service startup.
- [x] Expose active mode through operational endpoint.

#### Checkpoint tests
- [x] Startup mode test for each profile.
- [x] Operational status test returning active backend mode.

#### Pass criteria
- [x] Service starts successfully in all three modes.
- [x] Active mode is accurately reported and logged.

## Milestone 2: CRUD and Metadata Lifecycle

### Task 2.1 Implement document and artifact CRUD
- [ ] Implement create and read operations.
- [ ] Implement update operations with optimistic version checks.
- [ ] Implement delete operations with cascading artifact behavior.

#### Checkpoint tests
- [ ] CRUD contract test for create, read, update, and delete paths.
- [ ] Version conflict test for stale update requests.

#### Pass criteria
- [ ] CRUD operations satisfy contract responses across configured modes.
- [ ] Version conflicts are detected and handled with explicit error codes.

### Task 2.2 Implement metadata persistence adapter for PostgreSQL
- [ ] Implement relational writes for documents and artifacts.
- [ ] Implement status and audit metadata persistence.
- [ ] Add transactional boundaries for multi-record operations.

#### Checkpoint tests
- [ ] Transaction integrity test with forced mid-transaction error.
- [ ] Read-after-write consistency test for metadata retrieval.

#### Pass criteria
- [ ] Failed transactions rollback cleanly.
- [ ] Metadata retrieval reflects committed writes accurately.

## Milestone 3: Embedding Pipeline, Vector Retrieval, and Search APIs

### Task 3.1 Implement embedding generation pipeline
- [ ] Implement provider-agnostic embedding adapter inside FastAPI.
- [ ] Add batching, rate-limit handling, and retry policy for embedding calls.
- [ ] Persist embedding model metadata alongside generated vectors.

#### Checkpoint tests
- [ ] Embedding contract test with mock provider and one real provider profile.
- [ ] Determinism test for unchanged input, ensuring stable vector count and mapping.

#### Pass criteria
- [ ] FastAPI can generate embeddings from ingestion payload text without Project 2 embedding input.
- [ ] Embedding metadata is captured and queryable per artifact.

### Task 3.2 Implement Qdrant adapter and vector upsert path
- [ ] Add vector collection initialization logic.
- [ ] Implement upsert for FastAPI-generated vectors and payload metadata.
- [ ] Implement delete and update operations for vector records.

#### Checkpoint tests
- [ ] Vector upsert test with known embeddings and payload attributes.
- [ ] Vector delete test ensuring removed points are not returned in search.

#### Pass criteria
- [ ] Upsert and delete behavior is correct in repeated runs.
- [ ] Payload metadata is queryable for filter scenarios.

### Task 3.3 Implement retrieval endpoints
- [ ] Implement vector similarity search endpoint.
- [ ] Implement metadata-filtered retrieval endpoint.
- [ ] Implement source-context enrichment in response payload.

#### Checkpoint tests
- [ ] Relevance smoke test with seeded fixture vectors and expected top-k membership.
- [ ] Filter correctness test with strategy and source metadata predicates.

#### Pass criteria
- [ ] Top-k results include expected seeded neighbors.
- [ ] Filters constrain results correctly without leakage.

## Milestone 4: Operations, Security Baseline, and Release

### Task 4.1 Implement operational endpoints and telemetry hooks
- [ ] Add health and readiness endpoints.
- [ ] Add ingestion status lookup endpoints.
- [ ] Add request metrics and structured logging hooks.

#### Checkpoint tests
- [ ] Health endpoint test for service and backend dependencies.
- [ ] Telemetry smoke test verifying logs and key metrics are emitted.

#### Pass criteria
- [ ] Health and readiness are accurate under normal and degraded conditions.
- [ ] Telemetry contains trace id, endpoint, latency, and outcome fields.

### Task 4.2 Release candidate checkpoint
- [ ] Publish API usage guide for Project 2 and Streamlit UI and RAG (Project 4).
- [ ] Freeze API version for first integration release.
- [ ] Execute interoperability suite with Project 2 ingestion and Streamlit UI and RAG (Project 4) search.

#### Checkpoint tests
- [ ] End-to-end API interoperability test across create, search, update, and delete.
- [ ] Mode parity test across PostgreSQL-only, Qdrant-only, and combined mode.

#### Pass criteria
- [ ] Interoperability suite is green.
- [ ] Mode parity matrix passes supported feature expectations.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. API contracts are stable and consumable by ingestion and search projects.
3. Service supports the required backend modes with verifiable behavior.