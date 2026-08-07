# Document Transformation and Chunking Service (Project 1) Implementation Plan

## Objective
Build a document transformation service that uses Docling to convert raw PDF, DOC/DOCX, and HTML documents into normalized Markdown, then uses Chonkie to create semantic chunks and related retrieval artifacts for every ingested document: semantic chunks, contextual chunks, abstractive summaries, RAPTOR outputs, QA pairs, and factoids.

For LLM-backed derivative artifacts, the implementation shall use the Ollama model runner with on-prem models such as Llama, Gemma, or Qwen.

## Scope
- In scope: raw document conversion, Markdown normalization, strategy execution, metadata envelope, artifact versioning, deterministic pipeline stages, and strategy-level observability.
- Out of scope: persistence to final storage backends, API hosting, and UI.

## Milestone 1: Contracts and Preprocessing Foundation

### Task 1.1 Define canonical artifact contract
- [ ] Define required fields for document, artifact, lineage, and processing metadata.
- [ ] Define strategy-specific extension fields for all six artifact types.
- [ ] Define versioning fields for schema and strategy implementation.

#### Checkpoint tests
- [ ] Contract validation test: feed one valid artifact JSON per strategy and assert schema validation passes.
- [ ] Negative validation test: remove one required field and assert validation fails with clear error location.

#### Pass criteria
- [ ] All six valid payload samples pass schema validation.
- [ ] All invalid payload samples fail with deterministic error messages.

### Task 1.2 Build Docling-based raw document conversion pipeline
- [ ] Implement Docling ingestion for PDF, DOC/DOCX, and HTML source files.
- [ ] Convert extracted content to clean Markdown while preserving headings, lists, tables, links, and basic structural cues.
- [ ] Preserve mapping from normalized Markdown spans back to original source positions and page/section references.

#### Checkpoint tests
- [ ] Conversion test: one sample PDF, one DOC/DOCX, and one HTML file each convert to valid Markdown.
- [ ] Structure preservation test: headings, list items, and tables remain identifiable in converted output.

#### Pass criteria
- [ ] All supported input formats convert successfully into Markdown.
- [ ] Source position mapping is correct for at least three representative document samples.

## Milestone 2: Strategy Implementations

### Task 2.1 Implement Chonkie-based semantic and contextual chunkers
- [ ] Implement Chonkie semantic chunking on normalized Markdown with target token window and overlap settings.
- [ ] Implement contextual chunking that adds neighboring context and section headers to semantic chunks.
- [ ] Attach complete metadata envelope to both outputs, including source Markdown span references.

#### Checkpoint tests
- [ ] Semantic boundary test: chunk token counts remain inside configured limits.
- [ ] Context augmentation test: each contextual chunk includes expected adjacency fields.

#### Pass criteria
- [ ] All generated chunks meet token constraints.
- [ ] Context fields are present and non-empty for contextual artifacts.

### Task 2.2 Implement abstractive summary and RAPTOR strategies
- [ ] Implement abstractive summarization stage.
- [ ] Implement RAPTOR hierarchical aggregation with parent-child relationships.
- [ ] Integrate Ollama model runner for abstractive summary and RAPTOR generation using on-prem models such as Llama, Gemma, or Qwen.
- [ ] Record strategy model/provider metadata in outputs.

#### Checkpoint tests
- [ ] Hierarchy integrity test: every RAPTOR child references a valid parent or root.
- [ ] Summary length policy test: summaries satisfy configured length bounds.
- [ ] On-prem model test: configured Ollama model produces valid output for at least one supported model family.

#### Pass criteria
- [ ] RAPTOR graph has no broken parent-child links.
- [ ] Summary outputs satisfy min and max length policy.
- [ ] Ollama-backed generation works with at least one downloaded on-prem model.

### Task 2.3 Implement QA pairs and factoid extraction
- [ ] Generate QA pairs with provenance links to source spans.
- [ ] Extract factoids with deduplication strategy.
- [ ] Use Ollama model runner for QA pair and factoid generation with on-prem models such as Llama, Gemma, or Qwen.
- [ ] Add confidence score and extraction method fields.

#### Checkpoint tests
- [ ] QA provenance test: every answer points to at least one valid source span.
- [ ] Factoid dedup test: duplicate factoids are removed based on configured rule.
- [ ] Ollama response test: QA and factoid generation succeeds with a configured on-prem model.

#### Pass criteria
- [ ] QA pair artifacts are fully traceable to source text.
- [ ] Factoid output has no duplicate entries for identical canonical values.
- [ ] Derivative artifact generation completes successfully using Ollama and a supported on-prem model.

## Milestone 3: Orchestration and Packaging

### Task 3.1 Build multi-strategy execution orchestrator
- [ ] Create run coordinator that executes all six strategies per document.
- [ ] Add per-strategy timeout and retry policy.
- [ ] Emit strategy-level status for success, partial failure, and failure.

#### Checkpoint tests
- [ ] Orchestration test: one sample document yields outputs for all six strategies.
- [ ] Failure isolation test: forced failure in one strategy does not suppress outputs of successful strategies.

#### Pass criteria
- [ ] Six strategy outputs are produced in normal run path.
- [ ] Partial failure state is explicit and recoverable.

### Task 3.2 Produce export bundle for ingestion project
- [ ] Build final payload format expected by ingestion project.
- [ ] Include deterministic run identifier and artifact checksums.
- [ ] Package manifests for downstream integrity checks.

#### Checkpoint tests
- [ ] Bundle contract test: export payload validates against ingestion input schema.
- [ ] Checksum reproducibility test: same input document and config produce identical checksums.

#### Pass criteria
- [ ] Bundle validates with zero schema errors.
- [ ] Checksum generation is reproducible under identical inputs.

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