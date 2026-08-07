# Enterprise RAG Platform Design

## Document Purpose
This document defines the high-level design for a multi-project enterprise RAG platform. It translates the platform requirements into an architectural model that separates concerns across document transformation, ingestion, storage, service APIs, and user-facing search.

## Design Summary
The platform is organized into four primary projects connected through service interfaces and shared metadata conventions:
1. A document chunking and transformation project.
2. An ingestion/orchestration project that sends processed artifacts into storage through FastAPI.
3. A FastAPI platform service that manages CRUD, metadata, and configurable PostgreSQL/Qdrant interactions.
4. A Streamlit application that provides a RAG search experience through the API layer.

The initial system is single-tenant and local/dev-first. It is designed to support future operational hardening without changing the core project boundaries.

## Architecture Principles
- Keep document processing, storage orchestration, API management, and UI concerns in separate projects.
- Use shared metadata contracts to preserve traceability across all derived artifacts.
- Keep storage and model provider decisions configurable.
- Design for reprocessing and repeatable ingestion rather than one-time indexing only.
- Prefer provider-agnostic interfaces around embeddings and LLM-backed transformations.
- Use Ollama as the model runner for derivative artifact generation, with on-prem models such as Llama, Gemma, or Qwen.

## High-Level Architecture

The following diagram shows the core components, data paths, and control paths across the four projects.

```mermaid
flowchart LR
	U[Operators and Developers] --> C[Document Transformation and Chunking Service (Project 1)]
	D[(Source Documents)] --> C

	C -->|semantic chunks| I[Project 2: Ingestion and Storage Orchestration]
	C -->|contextual chunks| I
	C -->|abstractive summaries| I
	C -->|RAPTOR outputs| I
	C -->|QA pairs| I
	C -->|factoids| I

	I -->|create and update artifacts| A[FastAPI Backend Vector Manager (Project 3)]
	I -->|ingestion status and retries| A

	A -->|metadata CRUD| P[(PostgreSQL)]
	A -->|vector upsert and search payloads| Q[(Qdrant)]

	S[Streamlit UI and RAG (Project 4)] -->|search and filter requests| A
	A -->|ranked results with provenance| S

	A -->|health and config endpoints| U
```

### Document Transformation and Chunking Service (Project 1)
This project is responsible for converting raw PDF, DOC/DOCX, and HTML source documents into normalized Markdown with Docling, then creating retrieval-ready artifacts with Chonkie and related transformation strategies. It owns preprocessing, chunk creation, strategy-specific transformations, and common metadata generation.

Responsibilities:
- Accept source document content and metadata.
- Convert source documents to Markdown using Docling.
- Normalize and clean Markdown before transformation.
- Produce Chonkie-based semantic chunks.
- Produce contextual chunks.
- Produce abstractive summaries.
- Produce RAPTOR-style hierarchical summaries or rollups.
- Produce QA pairs.
- Produce factoids.
- Emit a canonical artifact payload for downstream ingestion.

Expected outputs:
- Document record with source metadata.
- One or more artifact collections by chunking strategy.
- Processing metadata such as strategy version, timestamps, and status.

### Project 2: Ingestion and Storage Orchestration
This project coordinates the transfer of transformed artifacts into the platform service for persistence. It owns submission workflows, retry behavior, idempotency logic, and operational status tracking.

Responsibilities:
- Receive processed outputs from the chunking project.
- Validate artifact payloads before storage submission.
- Call FastAPI endpoints for persistence.
- Track ingestion status and failures.
- Support re-ingestion for updated documents or chunking logic.

Expected outputs:
- Persisted records in relational and/or vector backends.
- Operational status records for success, failure, retry, and completion.

### FastAPI Backend Vector Manager (Project 3)
This service is the control plane for persistence and retrieval behavior. It exposes CRUD operations and abstracts backend choices through configuration.

Responsibilities:
- Expose create, read, update, and delete operations.
- Generate embeddings from chunk payload text using configured providers.
- Persist document and chunk metadata to PostgreSQL when enabled.
- Persist embeddings and searchable vectors to Qdrant when enabled.
- Support configuration-driven behavior for PostgreSQL-only, Qdrant-only, or combined operation.
- Provide search-facing APIs for vector retrieval and metadata filtering.
- Support admin and health endpoints for local/dev operations.

Expected outputs:
- Stable service contracts for ingestion and search clients.
- Consistent document lifecycle operations across supported backends.

### Streamlit UI and RAG (Project 4)
This project provides a lightweight user experience for validating search quality and demonstrating the platform.

Responsibilities:
- Accept user queries.
- Call FastAPI search endpoints.
- Display ranked retrieval results with provenance.
- Show chunk details, strategy origin, and source metadata.
- Support local/dev experimentation with filters and retrieval settings.

Expected outputs:
- Human-readable search interface for validation and demos.
- Observable query flow through the API layer.

## End-to-End Data Flow
1. A source document enters the chunking project.
2. The chunking project converts the raw document to Markdown with Docling, then preprocesses it and generates all required artifact types using Chonkie for semantic chunking.
3. Each derived artifact is tagged with source metadata, processing metadata, and strategy identity.
4. The ingestion project validates the output and submits records to FastAPI.
5. The FastAPI service writes metadata to PostgreSQL, vectors to Qdrant, or both depending on configuration.
6. The Streamlit application submits search requests to FastAPI.
7. FastAPI queries the configured search backend, enriches results with metadata, and returns ranked results.
8. Streamlit renders the results with source context and artifact provenance.

## Common Metadata Model
All derived artifacts should share a common metadata envelope to preserve traceability and simplify downstream storage.

Recommended metadata fields:
- document_id
- source_uri or source_name
- source_type
- ingestion_run_id
- chunk_strategy
- chunk_strategy_version
- artifact_id
- parent_artifact_id when hierarchical relationships exist
- page_number or logical_section when available
- created_at
- updated_at
- embedding_model identifier when embeddings are generated
- processing_status

This model allows the platform to track document lineage, support reprocessing, and correlate vector results back to source content.

## Chunking Strategy Design

### Semantic Chunks
Purpose:
- Split content into meaning-preserving segments optimized for retrieval.

Design notes:
- Should aim to preserve topical coherence.
- Suitable as a general-purpose retrieval artifact.

### Contextual Chunks
Purpose:
- Generate chunks that include additional local context such as neighboring passages, section titles, or document structure.

Design notes:
- Improves retrievability when isolated chunks lose meaning.
- Useful for structured or long-form documents.

### Abstractive Summaries
Purpose:
- Create concise summaries that capture the meaning of larger source sections.

Design notes:
- Use Ollama with on-prem models such as Llama, Gemma, or Qwen.
- Useful for high-level retrieval and compression.

### RAPTOR Outputs
Purpose:
- Build hierarchical summaries or rollups that represent the document at multiple abstraction levels.

Design notes:
- Use Ollama with on-prem models such as Llama, Gemma, or Qwen.
- Useful for tree-based or multi-resolution retrieval.
- Requires parent-child relationships in metadata.

### QA Pairs
Purpose:
- Generate anticipated question-answer pairs from the source content.

Design notes:
- Use Ollama with on-prem models such as Llama, Gemma, or Qwen.
- Useful for FAQ-style retrieval and direct answer matching.
- Quality-sensitive and should be validated against source provenance.

### Factoids
Purpose:
- Extract short, atomic facts from the document.

Design notes:
- Use Ollama with on-prem models such as Llama, Gemma, or Qwen.
- Useful for precise retrieval and structured evidence extraction.
- May require normalization rules to avoid duplication.

## Storage Design
The storage model should support both operational metadata and vector retrieval.

### PostgreSQL Role
Recommended uses:
- Document records
- Artifact metadata
- Processing status
- Audit-oriented operational information
- Configuration or lightweight administrative tables

### Qdrant Role
Recommended uses:
- Embedding vectors
- Searchable payloads for retrieval
- Metadata-assisted vector filtering

### Configuration Modes
The platform should support configuration-driven modes:
- PostgreSQL-only mode for metadata-first or limited local workflows.
- Qdrant-only mode for vector-centric experimentation.
- Combined mode for full document lifecycle plus vector retrieval.

Combined mode is the recommended target because it best matches the stated CRUD and search requirements.

## FastAPI Service Design
The FastAPI service should be split conceptually into storage APIs, retrieval APIs, and operational APIs.

### Storage APIs
Examples of responsibilities:
- Create document
- Create derived artifacts
- Update document or artifact state
- Delete document and associated artifacts
- Read document and artifact metadata

### Retrieval APIs
Examples of responsibilities:
- Vector search
- Metadata-filtered search
- Fetch artifact by identifier
- Fetch source context for a result

### Operational APIs
Examples of responsibilities:
- Health checks
- Configuration status
- Ingestion status lookup
- Reprocessing triggers for local/dev use

## Ingestion Design Considerations
- Ingestion should be idempotent where possible so retries do not create duplicate active records.
- The system should distinguish document identity from processing run identity.
- Reprocessing should allow a document to be re-chunked and re-indexed while retaining lineage.
- Partial failures should be visible through status records and logs.

## Streamlit Search Design
The Streamlit interface should serve as a validation tool and lightweight application shell.

Recommended UI capabilities:
- Query input box
- Search trigger with visible request state
- Result list with score and artifact type
- Expandable result cards showing chunk content and provenance
- Filters for artifact type or source metadata when available
- Visibility into which chunking strategy produced the result

## Security and Operational Design
- Initial operation assumes a trusted, single-tenant environment.
- Secrets should be provided through environment configuration.
- Service logs should avoid leaking sensitive content where possible.
- The design should allow future authentication and authorization layers without restructuring core project boundaries.

## Observability
The platform should emit enough telemetry for local/dev troubleshooting and future scale-up.

Recommended signals:
- Ingestion job start and completion events
- Per-strategy artifact counts
- Storage write success and failure counts
- Search request counts and latency
- Reprocessing events and failure reasons

## Deployment Path
Initial focus:
- Local/dev-first operation.
- Independently runnable projects.
- Configuration supplied through environment variables or config files.

Future path:
- Containerized services.
- Centralized observability.
- Stronger auth controls.
- Production-grade orchestration and scaling.

## Testing Strategy
- Unit tests for chunking logic, metadata assembly, and service adapters.
- Integration tests for FastAPI plus backend storage behavior.
- End-to-end tests covering ingest, persist, search, and delete workflows.
- Retrieval quality evaluation should be added in a later design phase.

## Recommended Repository Shape
A possible future structure is:
- docs/
- chunking-service/
- ingestion-service/
- platform-api/
- search-ui/
- shared-contracts/

This keeps metadata models and cross-project contracts explicit without merging responsibilities.

## Implementation Phases
1. Define shared document and artifact metadata contracts.
2. Build the chunking project with all required artifact strategies.
3. Build the FastAPI service with configurable storage adapters.
4. Build the ingestion/orchestration project against the API contracts.
5. Build the Streamlit search UI against retrieval endpoints.
6. Add observability, testing depth, and enterprise hardening.

## Open Design Decisions
- Exact document types and connectors are not yet defined.
- The specific embedding and LLM providers remain open.
- The consistency model between PostgreSQL and Qdrant needs to be finalized in detailed design.
- Search ranking and reranking logic are intentionally deferred.

## Related Document
- See the companion requirements document for goals, scope, constraints, and success criteria.