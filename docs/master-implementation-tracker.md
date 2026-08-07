# Enterprise RAG Master Implementation Tracker

## Purpose
This tracker links all project-level implementation plans and defines cross-project dependencies so milestone execution order is clear and testable.

## Linked Project Plans
1. [Project 1: Chunking and Transformation Plan](project-1-chunking-implementation-plan.md)
2. [Project 2: Ingestion and Storage Orchestration Plan](project-2-ingestion-implementation-plan.md)
3. [Project 3: FastAPI Platform Service Plan](project-3-fastapi-platform-implementation-plan.md)
4. [Project 4: Streamlit Search Application Plan](project-4-streamlit-search-implementation-plan.md)

## Dependency Summary
- Project 1 produces the chunk and metadata artifacts consumed by Project 2.
- Project 2 submits validated artifacts to Project 3 and depends on Project 3 API contracts.
- Project 3 provides CRUD, embedding/vectorization, and retrieval APIs consumed by Project 2 and Project 4.
- Project 4 depends on Project 3 retrieval APIs and is validated after Projects 1-3 provide stable ingest and search behavior.

## Cross-Project Dependency Matrix
| Depends On | Required By | Dependency Type | What Must Be Ready | Validation Checkpoint |
|---|---|---|---|---|
| Project 1 | Project 2 | Data contract | Artifact bundle schema, lineage metadata, strategy outputs | Project 2 intake schema test accepts Project 1 fixture bundle |
| Project 3 | Project 2 | API contract | Storage endpoint models, error envelopes, mode behavior | Project 2 contract integration test against Project 3 local endpoint |
| Project 2 | Project 3 | Integration behavior | Idempotent submission pattern, retry semantics, run identifiers | Project 3 interoperability suite includes Project 2 ingest flows |
| Project 3 | Project 4 | Retrieval API | Search endpoints, filter params, response provenance fields | Project 4 live integration test for top-k and filter behavior |
| Projects 1-3 | Project 4 | End-to-end data availability | Seeded corpus indexed and searchable | Project 4 end-to-end acceptance test passes |

## Milestone Synchronization Plan

### Wave 1: Contract and Foundation Alignment
- Project 1 Milestone 1
- Project 3 Milestone 1
- Project 2 Milestone 1

Exit gate:
- Project 1 artifact contract and Project 3 API contract are stable.
- Project 2 can validate and map Project 1 output to Project 3 input.

Test gate:
- Project 1 contract validation tests are green.
- Project 3 route and model validation tests are green.
- Project 2 intake schema and field parity tests are green.

### Wave 2: Core Processing and Persistence
- Project 1 Milestone 2
- Project 3 Milestone 2
- Project 2 Milestone 2

Exit gate:
- Project 1 emits complete strategy outputs.
- Project 2 performs idempotent submission without embeddings.
- Project 3 performs CRUD and metadata lifecycle behavior.

Test gate:
- Project 1 strategy-level tests are green.
- Project 2 replay and change-detection tests are green.
- Project 3 CRUD and transaction integrity tests are green.

### Wave 3: Search Readiness and Reliability
- Project 1 Milestone 3
- Project 3 Milestone 3
- Project 2 Milestone 3
- Project 4 Milestone 1 and Milestone 2

Exit gate:
- Project 1 exports ingestion-ready bundles.
- Project 3 generates embeddings and serves retrieval APIs.
- Project 2 handles retries and emits run telemetry.
- Project 4 renders ranked results and provenance.

Test gate:
- Project 1 bundle contract and checksum reproducibility tests are green.
- Project 3 embedding and retrieval tests are green.
- Project 2 retry/dead-letter and lifecycle metrics tests are green.
- Project 4 client contract and rendering/provenance tests are green.

### Wave 4: End-to-End Hardening and Release
- Project 1 Milestone 4
- Project 2 Milestone 4
- Project 3 Milestone 4
- Project 4 Milestone 3 and Milestone 4

Exit gate:
- All projects pass release candidate checkpoints.
- Interoperability across ingest, storage, search, and UI is stable.

Test gate:
- End-to-end ingest -> index -> query -> update -> delete acceptance suite is green.
- Mode parity checks pass for PostgreSQL-only, Qdrant-only, and combined modes where supported.
- Recovery drill from interrupted ingestion run passes without duplicate active records.

## Critical Path
1. Project 1 Milestone 1 -> Project 2 Milestone 1
2. Project 3 Milestone 1 -> Project 2 Milestone 1
3. Project 1 Milestone 2 -> Project 2 Milestone 2
4. Project 3 Milestone 2 -> Project 2 Milestone 2
5. Project 3 Milestone 3 -> Project 4 Milestone 1
6. Projects 1-3 Wave 3 completion -> Project 4 Milestone 4

## Parallelization Opportunities
- Project 1 Milestone 2 and Project 3 Milestone 2 can proceed in parallel after Wave 1 exit gate.
- Project 2 Milestone 2 can run concurrently once Project 1 bundle and Project 3 API contracts are frozen.
- Project 4 Milestone 1 UI foundation can begin with mocked Project 3 responses before live API readiness.

## Tracker Status Template
Use this checklist to track progress by wave and project.

### Wave Status
- [ ] Wave 1 complete
- [ ] Wave 2 complete
- [ ] Wave 3 complete
- [ ] Wave 4 complete

### Project Milestone Status
| Project | M1 | M2 | M3 | M4 |
|---|---|---|---|---|
| Project 1 | Not Started | Not Started | Not Started | Not Started |
| Project 2 | Not Started | Not Started | Not Started | Not Started |
| Project 3 | Not Started | Not Started | Not Started | Not Started |
| Project 4 | Not Started | Not Started | Not Started | Not Started |

## Change Control Rules
- Any contract change in Project 1 or Project 3 requires re-running Project 2 integration tests.
- Any retrieval response model change in Project 3 requires re-running Project 4 client contract and rendering tests.
- No wave can be marked complete unless all listed test gates for the wave are green.

## Recommended Update Cadence
- Update this tracker at least once per sprint.
- Update milestone status immediately after each checkpoint test pass.
- Record blockers with owner, impact, and target resolution date.