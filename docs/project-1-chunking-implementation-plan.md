# Project 1 Implementation Plan: Chunking and Transformation

## Objective
Build a document transformation service that uses Docling to convert raw PDF, DOC/DOCX, and HTML documents into normalized Markdown, then uses Chonkie to create semantic chunks and related retrieval artifacts for every ingested document: semantic chunks, contextual chunks, abstractive summaries, RAPTOR outputs, QA pairs, and factoids.

For LLM-backed derivative artifacts, the implementation shall use the Ollama model runner with on-prem models such as Llama, Gemma, or Qwen.

## Scope
- In scope: raw document conversion, Markdown normalization, strategy execution, metadata envelope, artifact versioning, deterministic pipeline stages, and strategy-level observability.
- Out of scope: persistence to final storage backends, API hosting, and UI.

## Milestone 1: Contracts and Preprocessing Foundation

### Task 1.1 Define canonical artifact contract
Subtasks:
1. Define required fields for document, artifact, lineage, and processing metadata.
2. Define strategy-specific extension fields for all six artifact types.
3. Define versioning fields for schema and strategy implementation.

Checkpoint tests:
1. Contract validation test: feed one valid artifact JSON per strategy and assert schema validation passes.
2. Negative validation test: remove one required field and assert validation fails with clear error location.

Pass criteria:
1. All six valid payload samples pass schema validation.
2. All invalid payload samples fail with deterministic error messages.

### Task 1.2 Build Docling-based raw document conversion pipeline
Subtasks:
1. Implement Docling ingestion for PDF, DOC/DOCX, and HTML source files.
2. Convert extracted content to clean Markdown while preserving headings, lists, tables, links, and basic structural cues.
3. Preserve mapping from normalized Markdown spans back to original source positions and page/section references.

Checkpoint tests:
1. Conversion test: one sample PDF, one DOC/DOCX, and one HTML file each convert to valid Markdown.
2. Structure preservation test: headings, list items, and tables remain identifiable in converted output.

Pass criteria:
1. All supported input formats convert successfully into Markdown.
2. Source position mapping is correct for at least three representative document samples.

## Milestone 2: Strategy Implementations

### Task 2.1 Implement Chonkie-based semantic and contextual chunkers
Subtasks:
1. Implement Chonkie semantic chunking on normalized Markdown with target token window and overlap settings.
2. Implement contextual chunking that adds neighboring context and section headers to semantic chunks.
3. Attach complete metadata envelope to both outputs, including source Markdown span references.

Checkpoint tests:
1. Semantic boundary test: chunk token counts remain inside configured limits.
2. Context augmentation test: each contextual chunk includes expected adjacency fields.

Pass criteria:
1. All generated chunks meet token constraints.
2. Context fields are present and non-empty for contextual artifacts.

### Task 2.2 Implement abstractive summary and RAPTOR strategies
Subtasks:
1. Implement abstractive summarization stage.
2. Implement RAPTOR hierarchical aggregation with parent-child relationships.
3. Integrate Ollama model runner for abstractive summary and RAPTOR generation using on-prem models such as Llama, Gemma, or Qwen.
4. Record strategy model/provider metadata in outputs.

Checkpoint tests:
1. Hierarchy integrity test: every RAPTOR child references a valid parent or root.
2. Summary length policy test: summaries satisfy configured length bounds.
3. On-prem model test: configured Ollama model produces valid output for at least one supported model family.

Pass criteria:
1. RAPTOR graph has no broken parent-child links.
2. Summary outputs satisfy min and max length policy.
3. Ollama-backed generation works with at least one downloaded on-prem model.

### Task 2.3 Implement QA pairs and factoid extraction
Subtasks:
1. Generate QA pairs with provenance links to source spans.
2. Extract factoids with deduplication strategy.
3. Use Ollama model runner for QA pair and factoid generation with on-prem models such as Llama, Gemma, or Qwen.
4. Add confidence score and extraction method fields.

Checkpoint tests:
1. QA provenance test: every answer points to at least one valid source span.
2. Factoid dedup test: duplicate factoids are removed based on configured rule.
3. Ollama response test: QA and factoid generation succeeds with a configured on-prem model.

Pass criteria:
1. QA pair artifacts are fully traceable to source text.
2. Factoid output has no duplicate entries for identical canonical values.
3. Derivative artifact generation completes successfully using Ollama and a supported on-prem model.

## Milestone 3: Orchestration and Packaging

### Task 3.1 Build multi-strategy execution orchestrator
Subtasks:
1. Create run coordinator that executes all six strategies per document.
2. Add per-strategy timeout and retry policy.
3. Emit strategy-level status for success, partial failure, and failure.

Checkpoint tests:
1. Orchestration test: one sample document yields outputs for all six strategies.
2. Failure isolation test: forced failure in one strategy does not suppress outputs of successful strategies.

Pass criteria:
1. Six strategy outputs are produced in normal run path.
2. Partial failure state is explicit and recoverable.

### Task 3.2 Produce export bundle for ingestion project
Subtasks:
1. Build final payload format expected by ingestion project.
2. Include deterministic run identifier and artifact checksums.
3. Package manifests for downstream integrity checks.

Checkpoint tests:
1. Bundle contract test: export payload validates against ingestion input schema.
2. Checksum reproducibility test: same input document and config produce identical checksums.

Pass criteria:
1. Bundle validates with zero schema errors.
2. Checksum generation is reproducible under identical inputs.

## Milestone 4: Quality Gates and Release Readiness

### Task 4.1 Add quality and regression suite
Subtasks:
1. Add representative fixture documents for at least three content types.
2. Add regression tests for artifact counts and metadata completeness.
3. Add smoke benchmark for per-document processing time.

Checkpoint tests:
1. Regression suite run with baseline snapshots.
2. Metadata completeness test requiring 100 percent required field coverage.

Pass criteria:
1. Baseline regression tests are green.
2. Metadata completeness is 100 percent for required fields.

### Task 4.2 Release candidate checkpoint
Subtasks:
1. Publish implementation notes and configuration defaults.
2. Freeze strategy version identifiers for downstream compatibility.
3. Produce handoff package for Project 2 integration.

Checkpoint tests:
1. Integration handshake test with Project 2 input validator.
2. Configuration sanity test across default and one alternate profile.

Pass criteria:
1. Handoff payload is accepted by Project 2 validators.
2. Configuration profiles load without runtime errors.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Every generated artifact is traceable to source content through metadata.
3. The project can produce ingestion-ready bundles for all six strategies in one run.