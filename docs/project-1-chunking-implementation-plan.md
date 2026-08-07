# Document Transformation and Chunking Service (Project 1) Implementation Plan

## Objective
Build a document transformation service that uses Docling to convert raw PDF, DOC/DOCX, and HTML documents into normalized Markdown, then uses Chonkie to create semantic chunks and related retrieval artifacts for every ingested document: semantic chunks, contextual chunks, abstractive summaries, RAPTOR outputs, QA pairs, and factoids.

For LLM-backed derivative artifacts, the implementation shall use the Ollama model runner with on-prem models such as Llama, Gemma, or Qwen.

## Scope
- In scope: raw document conversion, Markdown normalization, strategy execution, metadata envelope, artifact versioning, deterministic pipeline stages, and strategy-level observability.
- Out of scope: persistence to final storage backends, API hosting, and UI.

## Milestone 1: Contracts and Preprocessing Foundation

### Task 1.1 Define canonical artifact contract
- [x] Define required fields for document, artifact, lineage, and processing metadata.
- [x] Define strategy-specific extension fields for all six artifact types.
- [x] Define versioning fields for schema and strategy implementation.

#### Checkpoint tests
- [x] Contract validation test: feed one valid artifact JSON per strategy and assert schema validation passes.
- [x] Negative validation test: remove one required field and assert validation fails with clear error location.

#### Pass criteria
- [x] All six valid payload samples pass schema validation.
- [x] All invalid payload samples fail with deterministic error messages.

### Task 1.2 Build Docling-based raw document conversion pipeline
- [x] Implement Docling ingestion for PDF, DOC/DOCX, and HTML source files.
- [x] Convert extracted content to clean Markdown while preserving headings, lists, tables, links, and basic structural cues.
- [x] Preserve mapping from normalized Markdown spans back to original source positions and page/section references.

#### Checkpoint tests
- [x] Conversion test: one sample PDF, one DOC/DOCX, and one HTML file each convert to valid Markdown.
- [x] Structure preservation test: headings, list items, and tables remain identifiable in converted output.

#### Pass criteria
- [x] All supported input formats convert successfully into Markdown.
- [x] Source position mapping is correct for at least three representative document samples.

## Milestone 2: Strategy Implementations

### Task 2.1 Implement Chonkie-based semantic and contextual chunkers
- [x] Implement Chonkie semantic chunking on normalized Markdown with target token window and overlap settings.
- [x] Implement contextual chunking that adds neighboring context and section headers to semantic chunks.
- [x] Attach complete metadata envelope to both outputs, including source Markdown span references.

#### Checkpoint tests
- [x] Semantic boundary test: chunk token counts remain inside configured limits.
- [x] Context augmentation test: each contextual chunk includes expected adjacency fields.

#### Pass criteria
- [x] All generated chunks meet token constraints.
- [x] Context fields are present and non-empty for contextual artifacts.

### Task 2.2 Implement abstractive summary and RAPTOR strategies
- [x] Implement abstractive summarization stage.
- [x] Implement RAPTOR hierarchical aggregation with parent-child relationships.
- [x] Integrate Ollama model runner for abstractive summary and RAPTOR generation using on-prem models such as Llama, Gemma, or Qwen.
- [x] Record strategy model/provider metadata in outputs.

#### Checkpoint tests
- [x] Hierarchy integrity test: every RAPTOR child references a valid parent or root.
- [x] Summary length policy test: summaries satisfy configured length bounds.
- [x] On-prem model test: configured Ollama model produces valid output for at least one supported model family.

#### Pass criteria
- [x] RAPTOR graph has no broken parent-child links.
- [x] Summary outputs satisfy min and max length policy.
- [x] Ollama-backed generation works with at least one downloaded on-prem model.

### Task 2.3 Implement QA pairs and factoid extraction
- [x] Generate QA pairs with provenance links to source spans.
- [x] Extract factoids with deduplication strategy.
- [x] Use Ollama model runner for QA pair and factoid generation with on-prem models such as Llama, Gemma, or Qwen.
- [x] Add confidence score and extraction method fields.

#### Checkpoint tests
- [x] QA provenance test: every answer points to at least one valid source span.
- [x] Factoid dedup test: duplicate factoids are removed based on configured rule.
- [x] Ollama response test: QA and factoid generation succeeds with a configured on-prem model.

#### Pass criteria
- [x] QA pair artifacts are fully traceable to source text.
- [x] Factoid output has no duplicate entries for identical canonical values.
- [x] Derivative artifact generation completes successfully using Ollama and a supported on-prem model.

## Milestone 3: Orchestration and Packaging

### Task 3.1 Build multi-strategy execution orchestrator
- [x] Create run coordinator that executes all six strategies per document.
- [x] Add per-strategy timeout and retry policy.
- [x] Emit strategy-level status for success, partial failure, and failure.

#### Checkpoint tests
- [x] Orchestration test: one sample document yields outputs for all six strategies.
- [x] Failure isolation test: forced failure in one strategy does not suppress outputs of successful strategies.

#### Pass criteria
- [x] Six strategy outputs are produced in normal run path.
- [x] Partial failure state is explicit and recoverable.

### Task 3.2 Produce export bundle for ingestion project
- [x] Build final payload format expected by ingestion project.
- [x] Include deterministic run identifier and artifact checksums.
- [x] Package manifests for downstream integrity checks.

#### Checkpoint tests
- [x] Bundle contract test: export payload validates against ingestion input schema.
- [x] Checksum reproducibility test: same input document and config produce identical checksums.

#### Pass criteria
- [x] Bundle validates with zero schema errors.
- [x] Checksum generation is reproducible under identical inputs.

## Milestone 4: Quality Gates and Release Readiness

### Task 4.1 Add quality and regression suite
- [ ] Add representative fixture documents for at least three content types.
- [ ] Add regression tests for artifact counts and metadata completeness.
- [ ] Add smoke benchmark for per-document processing time.

#### Checkpoint tests
- [ ] Regression suite run with baseline snapshots.
- [ ] Metadata completeness test requiring 100 percent required field coverage.

#### Pass criteria
- [ ] Baseline regression tests are green.
- [ ] Metadata completeness is 100 percent for required fields.

### Task 4.2 Release candidate checkpoint
- [ ] Publish implementation notes and configuration defaults.
- [ ] Freeze strategy version identifiers for downstream compatibility.
- [ ] Produce handoff package for Project 2 integration.

#### Checkpoint tests
- [ ] Integration handshake test with Project 2 input validator.
- [ ] Configuration sanity test across default and one alternate profile.

#### Pass criteria
- [ ] Handoff payload is accepted by Project 2 validators.
- [ ] Configuration profiles load without runtime errors.

## Exit Criteria
1. All milestone checkpoint tests pass.
2. Every generated artifact is traceable to source content through metadata.
3. The project can produce ingestion-ready bundles for all six strategies in one run.