# CMS1450 Implementation Plan

Status: Implementation authorized; delivery status is in IMPLEMENTATION_STATUS.md. Keep authored files below 100 lines, splitting by responsibility.

## Selected stack

- Replit: React/TypeScript/Vite UI development and preview, with PDF.js for documents.
- FastAPI: typed APIs, document processing, revisions, validation and audit.
- LangGraph: checkpointed ingestion, human review and question workflows.
- LangChain: document/model interfaces, splitters, retrieval and answer composition.
- Pinecone: primary vector retrieval; local exact search remains a labeled offline adapter.
- SQLite and private backend files: prototype claim records, checkpoints and originals.

## Phase 1 Reference assets and contracts

Inspect the reference form, revision and reuse conditions; record source/checksum manifest. Use a labeled synthetic layout if redistribution is restricted. Define field, evidence, group, revision and adapter contracts. Validate every locator/subfield against CMS instructions. Create 12 synthetic cases, including degraded and multipage examples, with matching values and original-coordinate evidence.

Exit: complete registry, synthetic provenance and fixture/page consistency verified.

## Phase 2 Replit UI and claim review

Prepare a Replit build brief with screens, states, API contracts, example payloads and acceptance criteria. Build the split view against typed mocks first, then connect FastAPI through an environment-configured API URL. Select a reachable HTTPS backend or development proxy and explicit CORS origins. Keep source portable and mock/live modes visible.

Implement upload limits, page rendering, retryable status and fixture-checksum extraction. Add group editors, repeated tables, page controls, evidence navigation, accessible controls, saves, revision conflicts, audit, structural validation and export. Unmatched uploads remain unextracted.

Use a LangGraph ingestion workflow with persistent checkpoints, idempotent nodes and a review interrupt. Claim revisions remain authoritative when resuming. Keep model/Pinecone credentials on the backend and tracing off by default.

Exit: upload, correction, validation, save, reopen and export work in connected preview; arbitrary uploads never receive fabricated extraction.

## Phase 3 RAG and evidence answers

Serialize reviewed revisions into LangChain Documents with reversible source mappings. Implement token-based fixed and custom logical semantic splitters. Use shared embeddings and Pinecone settings, strategy namespaces, claim/revision filters and deterministic IDs. Verify visibility before marking an index ready; edits invalidate stale revisions.

Build the LangGraph question workflow with retrieval, optional local cross-encoder reranking, a LangChain answer adapter, abstention and citation validation. Connect the assistant drawer and evidence navigation. Label offline retrieval and lookup-only answers explicitly.

Exit: answers cite matching revisions and open their evidence; isolation, restart recovery and failure behavior are verified.

## Phase 4 Controlled comparison

Author and review 60 queries and gold evidence/answers; split by claim case into 15 development and 45 held-out queries. Define duplicate handling, unanswerable handling and hand-computable metric examples. Tune on development cases and freeze configuration.

Run all four conditions on immutable Pinecone snapshots after readiness checks. Record backend, namespace, models, packages, rankings, timings and seeds. Evaluate retrieval, answer support, equal-token budgets, paired deltas and uncertainty. Keep offline results separate.

Exit: chunking comparison and reranking impact reports have raw JSON/CSV and reproducible manifests, including negative or inconclusive findings.

## Phase 5 Real extraction extension

Agree provider, data handling, labeled images and accuracy targets. Add orientation, deskew, quality assessment, OCR/handwriting and mapping that can work without grid lines. Preserve inverse transforms and escalate uncertain fields. Benchmark field accuracy, row alignment, evidence localization and abstention by degradation type.

Exit: agreed thresholds are measured on actual extraction; curated demos are not used as accuracy evidence.

## Module boundaries and file size

Use `frontend/` for review/assistant UI; `backend/app/api/`, `models/`, `documents/`, `extraction/`, `claims/`, `workflows/`, `rag/` and `vectorstore/` for separate backend responsibilities. Keep fixtures, evaluation, reports, tests and documentation in their own directories.

Split UI into viewer, editor, tables, navigation and API modules; split graphs into state, nodes and graph construction. Extract shared contracts and helpers rather than creating oversized files. Check the under-100-line limit for every authored text/code file, including tests and reports. Binary assets have no line count; keep generated dependency locks/tool output separate from authored source and disclose any tool-required exception.

Prepare `docs/REPLIT_BUILD_BRIEF.md` during implementation, also below 100 lines. Break longer reports into an index and focused sections rather than hiding content in very long lines.

## Verification and risks

Verify locator coverage, row associations, coordinate transforms, upload rejection, persistence, conflicts, validation arithmetic, span mappings, claim isolation, stale-index blocking, citation support and metric calculations. Verify LangGraph restart/resume without duplicate writes and Pinecone filtering, visibility delays, deletion and network failures. Test Replit upload/render/save/citation flows and local offline operation.

| Risk | Response |
| --- | --- |
| Form revision or reuse restrictions | Record provenance and use synthetic layout if needed |
| Handwriting or absent lines | Combine layout signals and escalate uncertainty |
| Dummy data mistaken for OCR | Fixture matching and prominent mode labels |
| Larger semantic chunks bias metrics | Add equal-token retrieval comparison |
| Reranking adds delay without gains | Publish paired quality and latency changes |
| Stale answers after edits | Match claim/index revisions |
| Cloud connectivity or credentials fail | Explicit failure states and separately labeled offline mode |
| Sensitive data enters prototype | Use synthetic connected previews; scope regulated deployment separately |

## Review gate

Review the specification, this plan and tasks before implementation. Confirm real-extraction timing, answer model, backend connectivity and payer rules. No Replit project creation, paid resource provisioning, deployment or public publishing occurs in this planning update.
