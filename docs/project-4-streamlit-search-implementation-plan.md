# Project 4 Implementation Plan: Streamlit RAG Search Application

## Objective
Build a Streamlit application that enables users to query the platform, inspect ranked retrieval results, and validate artifact provenance through FastAPI search endpoints.

## Scope
- In scope: query UI, API client integration, result rendering, filtering, provenance visualization, and UX-level diagnostics.
- Out of scope: backend persistence logic and chunk generation.

## Milestone 1: UI Foundation and API Connectivity

### Task 1.1 Build base Streamlit layout and query controls
Subtasks:
1. Create layout for query input, parameter controls, and response state.
2. Add controls for top-k, strategy filter, and source filter placeholders.
3. Add visible loading and error states.

Checkpoint tests:
1. UI smoke test verifying all controls render.
2. Interaction test verifying query submit action is triggered.

Pass criteria:
1. All expected controls render in default view.
2. Submit action transitions to loading then response or error state.

### Task 1.2 Implement FastAPI client and request wiring
Subtasks:
1. Build API client abstraction with timeout and retry policy.
2. Implement request serialization for query and filters.
3. Parse response into UI-friendly data model.

Checkpoint tests:
1. Client contract test against mocked API responses.
2. Timeout and error handling test with simulated network delay and 5xx errors.

Pass criteria:
1. Client can parse successful responses and surface errors cleanly.
2. Network failures produce user-visible, actionable messages.

## Milestone 2: Result Rendering and Provenance

### Task 2.1 Implement ranked result cards
Subtasks:
1. Render ranked list with score, artifact type, and source identifier.
2. Add expandable content view for chunk text.
3. Add token or length indicators for result context size.

Checkpoint tests:
1. Rendering test for empty, single-result, and multi-result states.
2. Ranking order test ensuring UI preserves backend ranking sequence.

Pass criteria:
1. Result cards render correctly across all baseline states.
2. Ranking order in UI matches API response order.

### Task 2.2 Implement provenance and lineage views
Subtasks:
1. Show strategy type and strategy version for each result.
2. Show document-level provenance fields including source and section markers.
3. Add optional drill-down for related artifacts where available.

Checkpoint tests:
1. Provenance completeness test requiring all required lineage fields in rendered view.
2. Drill-down behavior test for related artifact links.

Pass criteria:
1. Users can inspect origin and strategy metadata for each result.
2. Lineage drill-down works for samples with related artifacts.

## Milestone 3: Search Controls and Validation Workflows

### Task 3.1 Implement filters and validation utilities
Subtasks:
1. Enable strategy, source type, and date-window filtering controls.
2. Add query history for current session.
3. Add export of response payload for debugging.

Checkpoint tests:
1. Filter behavior test confirming result set changes with each filter.
2. Export validity test ensuring exported payload is complete JSON.

Pass criteria:
1. Filters map correctly to API parameters.
2. Exported payload is valid and reproducible for bug reports.

### Task 3.2 Implement quality review workflow
Subtasks:
1. Add thumbs-up or thumbs-down relevance marker per result.
2. Store local feedback records for evaluation export.
3. Add simple review summary view for current session.

Checkpoint tests:
1. Feedback capture test for positive and negative marks.
2. Session summary accuracy test for counts and percentages.

Pass criteria:
1. Feedback actions are recorded reliably.
2. Summary metrics match captured events.

## Milestone 4: End-to-End Readiness and Release

### Task 4.1 Integrate with live FastAPI service
Subtasks:
1. Validate compatibility with retrieval endpoints from Project 3.
2. Validate support for backend mode differences where relevant.
3. Add resilient fallback messaging for partial service degradation.

Checkpoint tests:
1. Live integration test using seeded fixtures and expected top-k behavior.
2. Degradation test with unavailable backend dependency.

Pass criteria:
1. Live query path works under normal conditions.
2. Degraded states are handled with clear user messaging.

### Task 4.2 Release candidate checkpoint
Subtasks:
1. Publish usage guide for developers and reviewers.
2. Freeze UI response model for first release.
3. Execute end-to-end test from ingestion completion to search validation.

Checkpoint tests:
1. End-to-end acceptance test with fixture corpus from Project 1 and Project 2 pipeline.
2. Regression suite test for critical UI flows.

Pass criteria:
1. End-to-end acceptance path is green.
2. No critical regressions remain in query, render, filter, or feedback paths.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Users can run complete query-validation loops with provenance visibility.
3. The UI is stable for local/dev evaluation against the platform APIs.