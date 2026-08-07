# Project 2 Implementation Plan: Ingestion and Storage Orchestration

## Objective
Build an ingestion service that receives chunking outputs, prepares them for storage, calls FastAPI endpoints, and guarantees reliable, observable ingestion behavior.

## Scope
- In scope: payload intake, validation, payload normalization, idempotent submission, retry handling, and ingestion status tracking.
- Out of scope: final CRUD/search API ownership and end-user UI.

## Milestone 1: Intake and Validation

### Task 1.1 Build ingestion intake interface
Subtasks:
1. Define accepted bundle structure from Project 1.
2. Implement parser and validator for document-level and artifact-level records.
3. Persist transient run state for tracking ingest sessions.

Checkpoint tests:
1. Intake schema test: valid Project 1 bundle is accepted.
2. Invalid payload test: malformed artifact entries are rejected with indexed error details.

Pass criteria:
1. Valid bundles are accepted without warnings.
2. Invalid bundles return actionable validation errors.

### Task 1.2 Add normalization bridge for FastAPI payloads
Subtasks:
1. Map Project 1 artifact contract into FastAPI storage contract.
2. Ensure all required metadata fields are preserved.
3. Add deterministic ordering for artifact submission.

Checkpoint tests:
1. Field parity test: mapped payload retains all required source metadata fields.
2. Ordering determinism test: repeated mapping produces same ordered artifact list.

Pass criteria:
1. No metadata loss occurs during mapping.
2. Ordering is stable for identical inputs.

## Milestone 2: Payload Integrity and Idempotency

### Task 2.1 Finalize payload handoff contract for FastAPI-owned embeddings
Subtasks:
1. Define payload contract where raw text and metadata are sent to FastAPI for embedding generation.
2. Add strict field-level validation for artifact text, strategy metadata, and lineage metadata.
3. Add payload-size guardrails and chunk batching rules for FastAPI submission.

Checkpoint tests:
1. Contract compliance test: payload accepted by Project 3 input models without transformation errors.
2. Batch boundary test for minimum and maximum submission sizes.

Pass criteria:
1. Payload is accepted by FastAPI contract and contains no embedding fields.
2. Submission batching respects configured limits.

### Task 2.2 Implement idempotent write strategy
Subtasks:
1. Define idempotency key using document id, strategy, and artifact checksum.
2. Add duplicate detection before FastAPI submission.
3. Add conflict handling for stale or changed artifacts.

Checkpoint tests:
1. Replay test: submitting same bundle twice results in no duplicate active records.
2. Change detection test: modified artifact content is detected and routed to update path.

Pass criteria:
1. Replay path is idempotent.
2. Changed artifacts are correctly upserted.

## Milestone 3: Reliability and Observability

### Task 3.1 Implement retry and dead-letter policy
Subtasks:
1. Add transient failure retry with bounded exponential backoff.
2. Separate retryable and non-retryable API errors.
3. Store failed records in dead-letter queue structure for operator review.

Checkpoint tests:
1. Retry behavior test with simulated transient 5xx responses.
2. Dead-letter routing test with simulated hard validation failure.

Pass criteria:
1. Transient failures recover within retry budget when backend recovers.
2. Non-retryable failures are captured in dead-letter store with full context.

### Task 3.2 Implement run status and metrics
Subtasks:
1. Track run lifecycle states: started, in-progress, partial-failed, completed, failed.
2. Emit counters for accepted, rejected, retried, and persisted artifacts.
3. Emit timing metrics for parse, validate, submit, and total run duration.

Checkpoint tests:
1. Lifecycle transition test for success and partial-failure runs.
2. Metrics emission test verifying expected counters and durations are present.

Pass criteria:
1. Lifecycle states transition correctly.
2. Metrics are emitted consistently for every run.

## Milestone 4: Integration and Hardening

### Task 4.1 Integrate with FastAPI storage APIs
Subtasks:
1. Wire create and update submission paths.
2. Wire delete and reprocessing paths.
3. Add contract test fixtures shared with Project 3.

Checkpoint tests:
1. Contract integration test against Project 3 API mock and live local endpoint.
2. Reprocessing workflow test from old strategy version to new strategy version.

Pass criteria:
1. API calls are compatible with Project 3 contracts.
2. Reprocessing path completes without orphaned state.

### Task 4.2 Release candidate checkpoint
Subtasks:
1. Publish runbook for ingestion operations.
2. Define operational SLO targets for local/dev baseline.
3. Freeze interface version for Project 1 and Project 3 compatibility.

Checkpoint tests:
1. End-to-end dry run test from Project 1 bundle through FastAPI persistence.
2. Recovery drill test from forced mid-run interruption.

Pass criteria:
1. End-to-end ingestion succeeds for representative fixture set.
2. Interrupted run resumes or safely restarts with no duplicate writes.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Ingestion runs are idempotent, observable, and recoverable.
3. Project reliably submits valid payloads to Project 3 in supported modes.