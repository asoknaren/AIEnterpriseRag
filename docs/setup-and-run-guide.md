# AI Enterprise RAG Setup and Run Guide

## Purpose
This guide explains:
- How to collect and organize source documents
- How to set up the local environment
- How to run each project in this workspace
- What to expect as output at each stage

## Workspace Layout
- `data/raw/`: source documents before processing
- `data/processed/`: processed markdown/chunks/exports output
- `projects/document-transformation-chunking/`: Project 1
- `projects/ingestion-storage-orchestration/`: Project 2
- `projects/fastapi-backend-vector-manager/`: Project 3
- `projects/streamlit-ui-rag/`: Project 4

## Prerequisites
1. Python 3.10+ (3.12 recommended)
2. `pip` available in your shell
3. Windows PowerShell or compatible shell

## One-Time Environment Setup
From repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install each project in editable mode:

```powershell
python -m pip install -e .\projects\document-transformation-chunking
python -m pip install -e .\projects\ingestion-storage-orchestration
python -m pip install -e .\projects\fastapi-backend-vector-manager
python -m pip install -e .\projects\streamlit-ui-rag
```

Create local `.env` files from samples (per project):

```powershell
Copy-Item .\projects\document-transformation-chunking\.env.example .\projects\document-transformation-chunking\.env
Copy-Item .\projects\ingestion-storage-orchestration\.env.example .\projects\ingestion-storage-orchestration\.env
Copy-Item .\projects\fastapi-backend-vector-manager\.env.example .\projects\fastapi-backend-vector-manager\.env
Copy-Item .\projects\streamlit-ui-rag\.env.example .\projects\streamlit-ui-rag\.env
```

Then adjust values as needed for your local runtime profile.

Optional validation:

```powershell
python -m pytest .\projects\document-transformation-chunking\tests
python -m pytest .\projects\ingestion-storage-orchestration\tests
python -m pytest .\projects\fastapi-backend-vector-manager\tests
python -m pytest .\projects\streamlit-ui-rag\tests
```

Expected result:
- All test suites pass.
- You should see wave-based test files (`test_wave1_*` through `test_wave4_*`) passing.

## Configuration Settings by Project

Use this section as the source of truth for run-time settings before executing each project.

### Project 1: Document Transformation and Chunking
Required settings:
- No required environment variables.

Configurable settings:
- `profile_name` via strategy profile object.
  - Default profile: `default`
  - Alternate profile: `compact`
- `semantic_max_chars`
  - Default: `40`
  - Alternate: `30`
- `semantic_overlap`
  - Default: `10`
  - Alternate: `5`
- `summary_max_chars`
  - Default: `120`
  - Alternate: `90`
- `strategy_version`
  - Current release freeze: `4.0.0`
- `timeout_seconds` and `retry_attempts` for orchestrator runs.
  - Common Wave 4 handoff values: `timeout_seconds=2.0`, `retry_attempts=2`

Where defined:
- `projects/document-transformation-chunking/src/config_profiles.py`
- `projects/document-transformation-chunking/src/orchestrator.py`
- `projects/document-transformation-chunking/src/versioning.py`

### Project 2: Ingestion and Storage Orchestration
Required settings:
- No required environment variables.

Configurable settings:
- Interface compatibility freeze version.
  - `INTERFACE_VERSION=4.0.0`
- Batch sizing passed to handoff planner when preparing submissions.
  - Default in planner call path: `batch_size=20` unless overridden

Where defined:
- `projects/ingestion-storage-orchestration/src/interface_version.py`
- `projects/ingestion-storage-orchestration/src/submission/handoff.py`

### Project 3: FastAPI Backend Vector Manager
Required settings:
- `PYTHONPATH`
  - Must include `./projects/fastapi-backend-vector-manager/src` when running via `python -m uvicorn` from repo root.
- `APP_PROFILE`
  - Allowed values: `postgres-only`, `qdrant-only`, `combined`
  - Default if unset: `combined`

Configurable settings:
- Server host/port for local runs.
  - Typical values: `127.0.0.1:8000`

Where defined:
- `projects/fastapi-backend-vector-manager/src/app/config/settings.py`
- `projects/fastapi-backend-vector-manager/src/app/runtime/mode_selector.py`

### Project 4: Streamlit UI and RAG
Required settings:
- No required environment variables in current module-first implementation.

Configurable settings:
- Client timeout and retry policy.
  - `timeout_seconds` default: `2.0`
  - `max_retries` default: `2`
- Query control defaults.
  - `top_k=5`
  - `strategy_filter=all`
  - `source_filter=all`
  - Optional date filters: `date_from`, `date_to`

Where defined:
- `projects/streamlit-ui-rag/src/client.py`
- `projects/streamlit-ui-rag/src/ui_state.py`

### PowerShell Example: Apply Core Runtime Configuration

```powershell
# Run from repository root after activating .venv
$env:PYTHONPATH = ".\projects\fastapi-backend-vector-manager\src"
$env:APP_PROFILE = "combined"   # postgres-only | qdrant-only | combined
```

If you switch profile during testing, set `APP_PROFILE` again in the same terminal before starting FastAPI.

## How To Collect Source Docs

### 1. Gather files by source type
Place original files under `data/raw/` using source-specific folders that already exist:
- `data/raw/arxiv/`
- `data/raw/govinfo/`
- `data/raw/sec/`
- `data/raw/technical-docs/`

Recommended sub-organization:
- `pdf/` for PDF files
- `html/` for HTML captures
- `metadata/` for sidecar metadata JSON/CSV

Example:
- `data/raw/arxiv/pdf/paper-001.pdf`
- `data/raw/arxiv/metadata/paper-001.json`

### 2. Create/maintain source index
Update `data/manifests/source_index.csv` with one row per source document.

Recommended columns:
- `document_id`
- `source_type` (for example: `pdf`, `html`)
- `source_uri` (original URL or local path)
- `collection` (for example: `arxiv`, `govinfo`)
- `checksum` (optional but recommended)

Expected result:
- A complete source inventory exists before transformation.
- Each document has a stable `document_id` used across downstream projects.

### 3. Processed data expectations
After transformation/chunking runs, expect outputs under:
- `data/processed/markdown/`
- `data/processed/chunks/`
- `data/processed/exports/`

## Run Project 1: Document Transformation and Chunking
Directory:
- `projects/document-transformation-chunking`

Core outcome:
- Generate six artifact strategy outputs per document (semantic/contextual/summary/raptor/qa/factoids).
- Produce ingestion-ready bundle structures with lineage and metadata.

Project 1 configuration checklist:
- Confirm strategy profile defaults in `src/config_profiles.py`.
- Keep strategy version freeze aligned with `src/versioning.py` (`4.0.0`).

Run tests:

```powershell
python -m pytest .\projects\document-transformation-chunking\tests
```

Wave 4 quality/release checks are covered by:
- `test_wave4_quality_regression.py`
- `test_wave4_release_checkpoint.py`

Expected result:
- Green regression checks for artifact counts and metadata completeness.
- Handoff packaging validation with frozen strategy versions.

## Run Project 2: Ingestion and Storage Orchestration
Directory:
- `projects/ingestion-storage-orchestration`

Core outcome:
- Validate/mapping of Project 1 bundles into FastAPI-compatible payloads.
- Idempotent submission planning and reprocessing/recovery behavior.

Project 2 configuration checklist:
- Keep interface version aligned with `src/interface_version.py` (`4.0.0`).
- If you customize submission behavior, explicitly set planner `batch_size` in your integration code.

Run tests:

```powershell
python -m pytest .\projects\ingestion-storage-orchestration\tests
```

Wave 4 hardening checks are covered by:
- `test_wave4_fastapi_integration.py`
- `test_wave4_release_checkpoint.py`

Expected result:
- Contract compatibility with backend payload expectations.
- Recovery drill behavior (interruption and safe resume/restart semantics).

## Run Project 3: FastAPI Backend Vector Manager
Directory:
- `projects/fastapi-backend-vector-manager`

Core outcome:
- Serve CRUD, embedding upsert, similarity/filter search, ops/health/readiness, and ingestion status endpoints.

Project 3 configuration checklist:
- Set `PYTHONPATH` for local module imports.
- Set `APP_PROFILE` to one of: `postgres-only`, `qdrant-only`, `combined`.

### Start API server
From repo root:

```powershell
$env:PYTHONPATH = ".\projects\fastapi-backend-vector-manager\src"
$env:APP_PROFILE = "combined"  # or postgres-only / qdrant-only
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Key endpoints to verify:
- `GET /api/v1/health`
- `GET /api/v1/readiness`
- `GET /api/v1/ops/mode`
- `POST /api/v1/embeddings/upsert`
- `POST /api/v1/search/similarity`
- `POST /api/v1/search/filter`
- `GET /api/v1/ingestion/status/{run_id}`

Run tests:

```powershell
python -m pytest .\projects\fastapi-backend-vector-manager\tests
```

Expected result:
- API tests pass across wave suites.
- Mode parity checks pass for `postgres-only`, `qdrant-only`, and `combined` profiles.

## Run Project 4: Streamlit UI and RAG
Directory:
- `projects/streamlit-ui-rag`

Core outcome:
- Query flow, ranked rendering, provenance visibility, filtering controls, history/export, feedback summary, and degraded-state handling.

Project 4 configuration checklist:
- Tune client `timeout_seconds` and `max_retries` in `ClientConfig` if backend latency differs.
- Confirm default query controls (`top_k`, filters, date window) in `src/ui_state.py`.

Run tests:

```powershell
python -m pytest .\projects\streamlit-ui-rag\tests
```

Run Streamlit app (if/when entry app script is added):

```powershell
streamlit run <app_entrypoint.py>
```

Note:
- Current implementation is module-first and test-driven (`src/ui_state.py`, `src/app_logic.py`, `src/client.py`, `src/rendering.py`).
- If an app entrypoint is not yet present, use tests as the executable validation path.

Expected result:
- Wave 3/4 tests confirm filter mapping, export payload validity, feedback metrics, and degradation messaging.

## End-to-End Local Execution Order
1. Collect source docs and update `data/manifests/source_index.csv`.
2. Run Project 1 tests (transformation/chunking and handoff generation checks).
3. Start Project 3 FastAPI service in one terminal.
4. Run Project 2 tests (integration/recovery against backend contracts).
5. Run Project 4 tests (search client/rendering/validation flows).

Expected overall result:
- End-to-end ingest/index/query/update/delete acceptance behavior is verified through Wave 4 test suites and project checkpoints.

## Quick Troubleshooting
- `ModuleNotFoundError` when running FastAPI or tests:
  - Ensure venv is active.
  - Ensure `PYTHONPATH` includes the correct `src` folder for project-local imports.
- FastAPI profile errors:
  - Verify `APP_PROFILE` is one of: `postgres-only`, `qdrant-only`, `combined`.
- Streamlit run command fails:
  - Confirm there is an app entrypoint script; otherwise run test suite for validation.

## Reference Documents
- `docs/master-implementation-tracker.md`
- `docs/project-1-chunking-implementation-plan.md`
- `docs/project-2-ingestion-implementation-plan.md`
- `docs/project-3-fastapi-platform-implementation-plan.md`
- `docs/project-4-streamlit-search-implementation-plan.md`
