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
- [x] Define payload contract where raw text and metadata are sent to FastAPI for embedding generation.
- [x] Add strict field-level validation for artifact text, strategy metadata, and lineage metadata.
- [x] Add payload-size guardrails and chunk batching rules for FastAPI submission.

#### Checkpoint tests
- [x] Contract compliance test: payload accepted by FastAPI Backend Vector Manager (Project 3) input models without transformation errors.
- [x] Batch boundary test for minimum and maximum submission sizes.

#### Pass criteria
- [x] Payload is accepted by FastAPI contract and contains no embedding fields.
- [x] Submission batching respects configured limits.

### Task 2.2 Implement idempotent write strategy
- [x] Define idempotency key using document id, strategy, and artifact checksum.
- [x] Add duplicate detection before FastAPI submission.
- [x] Add conflict handling for stale or changed artifacts.

#### Checkpoint tests
- [x] Replay test: submitting same bundle twice results in no duplicate active records.
- [x] Change detection test: modified artifact content is detected and routed to update path.

#### Pass criteria
- [x] Replay path is idempotent.
- [x] Changed artifacts are correctly upserted.

## Milestone 3: Reliability and Observability

### Task 3.1 Implement retry and dead-letter policy
- [x] Add transient failure retry with bounded exponential backoff.
- [x] Separate retryable and non-retryable API errors.
- [x] Store failed records in dead-letter queue structure for operator review.

#### Checkpoint tests
- [x] Retry behavior test with simulated transient 5xx responses.
- [x] Dead-letter routing test with simulated hard validation failure.

#### Pass criteria
- [x] Transient failures recover within retry budget when backend recovers.
- [x] Non-retryable failures are captured in dead-letter store with full context.

### Task 3.2 Implement run status and metrics
- [x] Track run lifecycle states: started, in-progress, partial-failed, completed, failed.
- [x] Emit counters for accepted, rejected, retried, and persisted artifacts.
- [x] Emit timing metrics for parse, validate, submit, and total run duration.

#### Checkpoint tests
- [x] Lifecycle transition test for success and partial-failure runs.
- [x] Metrics emission test verifying expected counters and durations are present.

#### Pass criteria
- [x] Lifecycle states transition correctly.
- [x] Metrics are emitted consistently for every run.

## Milestone 4: Integration and Hardening

### Task 4.1 Integrate with FastAPI storage APIs
- [x] Wire create and update submission paths.
- [x] Wire delete and reprocessing paths.
- [x] Add contract test fixtures shared with FastAPI Backend Vector Manager (Project 3).

#### Checkpoint tests
- [x] Contract integration test against FastAPI Backend Vector Manager (Project 3) API mock and live local endpoint.
- [x] Reprocessing workflow test from old strategy version to new strategy version.

#### Pass criteria
- [x] API calls are compatible with FastAPI Backend Vector Manager (Project 3) contracts.
- [x] Reprocessing path completes without orphaned state.

### Task 4.2 Release candidate checkpoint
- [x] Publish runbook for ingestion operations.
- [x] Define operational SLO targets for local/dev baseline.
- [x] Freeze interface version for Document Transformation and Chunking Service (Project 1) and FastAPI Backend Vector Manager (Project 3) compatibility.

#### Checkpoint tests
- [x] End-to-end dry run test from Document Transformation and Chunking Service (Project 1) bundle through FastAPI persistence.
- [x] Recovery drill test from forced mid-run interruption.

#### Pass criteria
- [x] End-to-end ingestion succeeds for representative fixture set.
- [x] Interrupted run resumes or safely restarts with no duplicate writes.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Ingestion runs are idempotent, observable, and recoverable.
3. Project reliably submits valid payloads to FastAPI Backend Vector Manager (Project 3) in supported modes.