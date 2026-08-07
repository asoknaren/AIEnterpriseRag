# Streamlit UI and RAG (Project 4) Implementation Plan

## Objective
Build a Streamlit application that enables users to query the platform, inspect ranked retrieval results, and validate artifact provenance through FastAPI search endpoints.

## Scope
- In scope: query UI, API client integration, result rendering, filtering, provenance visualization, and UX-level diagnostics.
- Out of scope: backend persistence logic and chunk generation.

## Milestone 1: UI Foundation and API Connectivity

### Task 1.1 Build base Streamlit layout and query controls
- [ ] Create layout for query input, parameter controls, and response state.
- [ ] Add controls for top-k, strategy filter, and source filter placeholders.
- [ ] Add visible loading and error states.

#### Checkpoint tests
- [ ] UI smoke test verifying all controls render.
- [ ] Interaction test verifying query submit action is triggered.

#### Pass criteria
- [ ] All expected controls render in default view.
- [ ] Submit action transitions to loading then response or error state.

### Task 1.2 Implement FastAPI client and request wiring
- [ ] Build API client abstraction with timeout and retry policy.
- [ ] Implement request serialization for query and filters.
- [ ] Parse response into UI-friendly data model.

#### Checkpoint tests
- [ ] Client contract test against mocked API responses.
- [ ] Timeout and error handling test with simulated network delay and 5xx errors.

#### Pass criteria
- [ ] Client can parse successful responses and surface errors cleanly.
- [ ] Network failures produce user-visible, actionable messages.

## Milestone 2: Result Rendering and Provenance

### Task 2.1 Implement ranked result cards
- [ ] Render ranked list with score, artifact type, and source identifier.
- [ ] Add expandable content view for chunk text.
- [ ] Add token or length indicators for result context size.

#### Checkpoint tests
- [ ] Rendering test for empty, single-result, and multi-result states.
- [ ] Ranking order test ensuring UI preserves backend ranking sequence.

#### Pass criteria
- [ ] Result cards render correctly across all baseline states.
- [ ] Ranking order in UI matches API response order.

### Task 2.2 Implement provenance and lineage views
- [ ] Show strategy type and strategy version for each result.
- [ ] Show document-level provenance fields including source and section markers.
- [ ] Add optional drill-down for related artifacts where available.

#### Checkpoint tests
- [ ] Provenance completeness test requiring all required lineage fields in rendered view.
- [ ] Drill-down behavior test for related artifact links.

#### Pass criteria
- [ ] Users can inspect origin and strategy metadata for each result.
- [ ] Lineage drill-down works for samples with related artifacts.

## Milestone 3: Search Controls and Validation Workflows

### Task 3.1 Implement filters and validation utilities
- [ ] Enable strategy, source type, and date-window filtering controls.
- [ ] Add query history for current session.
- [ ] Add export of response payload for debugging.

#### Checkpoint tests
- [ ] Filter behavior test confirming result set changes with each filter.
- [ ] Export validity test ensuring exported payload is complete JSON.

#### Pass criteria
- [ ] Filters map correctly to API parameters.
- [ ] Exported payload is valid and reproducible for bug reports.

### Task 3.2 Implement quality review workflow
- [ ] Add thumbs-up or thumbs-down relevance marker per result.
- [ ] Store local feedback records for evaluation export.
- [ ] Add simple review summary view for current session.

#### Checkpoint tests
- [ ] Feedback capture test for positive and negative marks.
- [ ] Session summary accuracy test for counts and percentages.

#### Pass criteria
- [ ] Feedback actions are recorded reliably.
- [ ] Summary metrics match captured events.

## Milestone 4: End-to-End Readiness and Release

### Task 4.1 Integrate with live FastAPI service
- [ ] Validate compatibility with retrieval endpoints from FastAPI Backend Vector Manager (Project 3).
- [ ] Validate support for backend mode differences where relevant.
- [ ] Add resilient fallback messaging for partial service degradation.

#### Checkpoint tests
- [ ] Live integration test using seeded fixtures and expected top-k behavior.
- [ ] Degradation test with unavailable backend dependency.

#### Pass criteria
- [ ] Live query path works under normal conditions.
- [ ] Degraded states are handled with clear user messaging.

### Task 4.2 Release candidate checkpoint
- [ ] Publish usage guide for developers and reviewers.
- [ ] Freeze UI response model for first release.
- [ ] Execute end-to-end test from ingestion completion to search validation.

#### Checkpoint tests
- [ ] End-to-end acceptance test with fixture corpus from Document Transformation and Chunking Service (Project 1) and Project 2 pipeline.
- [ ] Regression suite test for critical UI flows.

#### Pass criteria
- [ ] End-to-end acceptance path is green.
- [ ] No critical regressions remain in query, render, filter, or feedback paths.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Users can run complete query-validation loops with provenance visibility.
3. The UI is stable for local/dev evaluation against the platform APIs.