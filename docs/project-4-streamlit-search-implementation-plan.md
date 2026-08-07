# Streamlit UI and RAG (Project 4) Implementation Plan

## Objective
Build a Streamlit application that enables users to query the platform, inspect ranked retrieval results, and validate artifact provenance through FastAPI search endpoints.

## Scope
- In scope: query UI, API client integration, result rendering, filtering, provenance visualization, and UX-level diagnostics.
- Out of scope: backend persistence logic and chunk generation.

## Milestone 1: UI Foundation and API Connectivity

### Task 1.1 Build base Streamlit layout and query controls
- [x] Create layout for query input, parameter controls, and response state.
- [x] Add controls for top-k, strategy filter, and source filter placeholders.
- [x] Add visible loading and error states.

#### Checkpoint tests
- [x] UI smoke test verifying all controls render.
- [x] Interaction test verifying query submit action is triggered.

#### Pass criteria
- [x] All expected controls render in default view.
- [x] Submit action transitions to loading then response or error state.

### Task 1.2 Implement FastAPI client and request wiring
- [x] Build API client abstraction with timeout and retry policy.
- [x] Implement request serialization for query and filters.
- [x] Parse response into UI-friendly data model.

#### Checkpoint tests
- [x] Client contract test against mocked API responses.
- [x] Timeout and error handling test with simulated network delay and 5xx errors.

#### Pass criteria
- [x] Client can parse successful responses and surface errors cleanly.
- [x] Network failures produce user-visible, actionable messages.

## Milestone 2: Result Rendering and Provenance

### Task 2.1 Implement ranked result cards
- [x] Render ranked list with score, artifact type, and source identifier.
- [x] Add expandable content view for chunk text.
- [x] Add token or length indicators for result context size.

#### Checkpoint tests
- [x] Rendering test for empty, single-result, and multi-result states.
- [x] Ranking order test ensuring UI preserves backend ranking sequence.

#### Pass criteria
- [x] Result cards render correctly across all baseline states.
- [x] Ranking order in UI matches API response order.

### Task 2.2 Implement provenance and lineage views
- [x] Show strategy type and strategy version for each result.
- [x] Show document-level provenance fields including source and section markers.
- [x] Add optional drill-down for related artifacts where available.

#### Checkpoint tests
- [x] Provenance completeness test requiring all required lineage fields in rendered view.
- [x] Drill-down behavior test for related artifact links.

#### Pass criteria
- [x] Users can inspect origin and strategy metadata for each result.
- [x] Lineage drill-down works for samples with related artifacts.

## Milestone 3: Search Controls and Validation Workflows

### Task 3.1 Implement filters and validation utilities
- [x] Enable strategy, source type, and date-window filtering controls.
- [x] Add query history for current session.
- [x] Add export of response payload for debugging.

#### Checkpoint tests
- [x] Filter behavior test confirming result set changes with each filter.
- [x] Export validity test ensuring exported payload is complete JSON.

#### Pass criteria
- [x] Filters map correctly to API parameters.
- [x] Exported payload is valid and reproducible for bug reports.

### Task 3.2 Implement quality review workflow
- [x] Add thumbs-up or thumbs-down relevance marker per result.
- [x] Store local feedback records for evaluation export.
- [x] Add simple review summary view for current session.

#### Checkpoint tests
- [x] Feedback capture test for positive and negative marks.
- [x] Session summary accuracy test for counts and percentages.

#### Pass criteria
- [x] Feedback actions are recorded reliably.
- [x] Summary metrics match captured events.

## Milestone 4: End-to-End Readiness and Release

### Task 4.1 Integrate with live FastAPI service
- [x] Validate compatibility with retrieval endpoints from FastAPI Backend Vector Manager (Project 3).
- [x] Validate support for backend mode differences where relevant.
- [x] Add resilient fallback messaging for partial service degradation.

#### Checkpoint tests
- [x] Live integration test using seeded fixtures and expected top-k behavior.
- [x] Degradation test with unavailable backend dependency.

#### Pass criteria
- [x] Live query path works under normal conditions.
- [x] Degraded states are handled with clear user messaging.

### Task 4.2 Release candidate checkpoint
- [x] Publish usage guide for developers and reviewers.
- [x] Freeze UI response model for first release.
- [x] Execute end-to-end test from ingestion completion to search validation.

#### Checkpoint tests
- [x] End-to-end acceptance test with fixture corpus from Document Transformation and Chunking Service (Project 1) and Project 2 pipeline.
- [x] Regression suite test for critical UI flows.

#### Pass criteria
- [x] End-to-end acceptance path is green.
- [x] No critical regressions remain in query, render, filter, or feedback paths.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Users can run complete query-validation loops with provenance visibility.
3. The UI is stable for local/dev evaluation against the platform APIs.