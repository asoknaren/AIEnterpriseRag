# Project 2 Implementation Plan: Ingestion and Storage Orchestration

## Objective
Build an ingestion service that receives chunking outputs, prepares them for storage, calls FastAPI endpoints, and guarantees reliable, observable ingestion behavior.

## Scope
- In scope: payload intake, validation, payload normalization, idempotent submission, retry handling, and ingestion status tracking.
- Out of scope: final CRUD/search API ownership and end-user UI.

## Milestone 1: Intake and Validation

### Task 1.1 Build ingestion intake interface
- [x] Define accepted bundle structure from Document Transformation and Chunking Service (Project 1).
- [x] Implement parser and validator for document-level and artifact-level records.
- [x] Persist transient run state for tracking ingest sessions.

#### Checkpoint tests
- [x] Intake schema test: valid Document Transformation and Chunking Service (Project 1) bundle is accepted.
- [x] Invalid payload test: malformed artifact entries are rejected with indexed error details.

#### Pass criteria
- [x] Valid bundles are accepted without warnings.
- [x] Invalid bundles return actionable validation errors.

### Task 1.2 Add normalization bridge for FastAPI payloads
- [x] Map Document Transformation and Chunking Service (Project 1) artifact contract into FastAPI storage contract.
- [x] Ensure all required metadata fields are preserved.
- [x] Add deterministic ordering for artifact submission.

#### Checkpoint tests
- [x] Field parity test: mapped payload retains all required source metadata fields.
- [x] Ordering determinism test: repeated mapping produces same ordered artifact list.

#### Pass criteria
- [x] No metadata loss occurs during mapping.
- [x] Ordering is stable for identical inputs.

## Milestone 2: Payload Integrity and Idempotency

### Task 2.1 Finalize payload handoff contract for FastAPI-owned embeddings
- [ ] Define payload contract where raw text and metadata are sent to FastAPI for embedding generation.
- [ ] Add strict field-level validation for artifact text, strategy metadata, and lineage metadata.
- [ ] Add payload-size guardrails and chunk batching rules for FastAPI submission.

#### Checkpoint tests
- [ ] Contract compliance test: payload accepted by FastAPI Backend Vector Manager (Project 3) input models without transformation errors.
- [ ] Batch boundary test for minimum and maximum submission sizes.

#### Pass criteria
- [ ] Payload is accepted by FastAPI contract and contains no embedding fields.
- [ ] Submission batching respects configured limits.

### Task 2.2 Implement idempotent write strategy
- [ ] Define idempotency key using document id, strategy, and artifact checksum.
- [ ] Add duplicate detection before FastAPI submission.
- [ ] Add conflict handling for stale or changed artifacts.

#### Checkpoint tests
- [ ] Replay test: submitting same bundle twice results in no duplicate active records.
- [ ] Change detection test: modified artifact content is detected and routed to update path.

#### Pass criteria
- [ ] Replay path is idempotent.
- [ ] Changed artifacts are correctly upserted.

## Milestone 3: Reliability and Observability

### Task 3.1 Implement retry and dead-letter policy
- [ ] Add transient failure retry with bounded exponential backoff.
- [ ] Separate retryable and non-retryable API errors.
- [ ] Store failed records in dead-letter queue structure for operator review.

#### Checkpoint tests
- [ ] Retry behavior test with simulated transient 5xx responses.
- [ ] Dead-letter routing test with simulated hard validation failure.

#### Pass criteria
- [ ] Transient failures recover within retry budget when backend recovers.
- [ ] Non-retryable failures are captured in dead-letter store with full context.

### Task 3.2 Implement run status and metrics
- [ ] Track run lifecycle states: started, in-progress, partial-failed, completed, failed.
- [ ] Emit counters for accepted, rejected, retried, and persisted artifacts.
- [ ] Emit timing metrics for parse, validate, submit, and total run duration.

#### Checkpoint tests
- [ ] Lifecycle transition test for success and partial-failure runs.
- [ ] Metrics emission test verifying expected counters and durations are present.

#### Pass criteria
- [ ] Lifecycle states transition correctly.
- [ ] Metrics are emitted consistently for every run.

## Milestone 4: Integration and Hardening

### Task 4.1 Integrate with FastAPI storage APIs
- [ ] Wire create and update submission paths.
- [ ] Wire delete and reprocessing paths.
- [ ] Add contract test fixtures shared with FastAPI Backend Vector Manager (Project 3).

#### Checkpoint tests
- [ ] Contract integration test against FastAPI Backend Vector Manager (Project 3) API mock and live local endpoint.
- [ ] Reprocessing workflow test from old strategy version to new strategy version.

#### Pass criteria
- [ ] API calls are compatible with FastAPI Backend Vector Manager (Project 3) contracts.
- [ ] Reprocessing path completes without orphaned state.

### Task 4.2 Release candidate checkpoint
- [ ] Publish runbook for ingestion operations.
- [ ] Define operational SLO targets for local/dev baseline.
- [ ] Freeze interface version for Document Transformation and Chunking Service (Project 1) and FastAPI Backend Vector Manager (Project 3) compatibility.

#### Checkpoint tests
- [ ] End-to-end dry run test from Document Transformation and Chunking Service (Project 1) bundle through FastAPI persistence.
- [ ] Recovery drill test from forced mid-run interruption.

#### Pass criteria
- [ ] End-to-end ingestion succeeds for representative fixture set.
- [ ] Interrupted run resumes or safely restarts with no duplicate writes.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Ingestion runs are idempotent, observable, and recoverable.
3. Project reliably submits valid payloads to FastAPI Backend Vector Manager (Project 3) in supported modes.