# CMS1450 Implementation Tasks

Status: Implementation authorized. Checked tasks are implemented locally; see IMPLEMENTATION_STATUS.md for verification and remaining boundaries.

File rule: keep every authored file below 100 lines. Split modules, tests and reports by responsibility; do not compress content into oversized lines. Check line counts before completing each task.

## Review gate

- [x] R1 Specification and plan reviewed; user authorized implementation.
- [x] R2 Curated extraction first; real extraction remains a separate milestone.
- [x] R3 Replit-ready UI, LangGraph/LangChain/Pinecone stack, local model adapters and same-origin backend selected; live Pinecone credentials remain unset.

## Phase 1 Reference assets and data contracts

- [x] T01 Retrieve and inspect the CMS-1450 reference; record source, revision, checksum and reuse conditions. Depends on R1.
- [x] T02 Define typed documents, claims, fields, groups, evidence, revisions, audit and extraction adapter contracts. Depends on R1.
- [ ] T03 Build the complete locator/subfield registry with group ownership, reserved entries and repeatable row identities. Depends on T01–T02.
- [x] T04 Curate 12 synthetic cases with matching pages, values and evidence regions; include degraded and multipage examples and a manifest. Depends on T03.
- [x] T05 Verify fixture/page consistency, synthetic provenance and coordinate conventions. Depends on T04.

## Phase 2 Upload and editable review

- [x] T06 Replit build brief, portable frontend/backend, pinned dependencies, fixture-backed API contracts, server configuration, CORS and setup docs implemented. Separate mock-only frontend mode was not needed for the working fixture API.
- [x] T07 Implement bounded PDF/image upload, validation, page rendering and retryable job status using a checkpointed LangGraph ingestion workflow. Verify idempotent retries and restart recovery. Depends on T06.
- [x] T08 Implement checksum-matched curated extraction and explicit unmatched-upload behavior. Depends on T05 and T07.
- [x] T09 Replit-ready split view, PDF.js, pages, zoom, rotation and accessible controls implemented and tested locally. Actual Replit preview remains a hosting follow-up.
- [x] T10 Build group navigation, typed editable fields and repeatable service/payer/code tables. Depends on T03, T08 and T09.
- [x] T11 Connect source regions and field selection; handle absent evidence and transformed pages. Depends on T10.
- [x] T12 Implement revision-aware saves, conflict handling, audit history, reopen and JSON export. Depends on T10.
- [x] T13 Add structural validation, review states and explicit issue acknowledgments; wire revision-aware human-review interrupt/resume to the ingestion graph. Depends on T12 and T07.
- [x] T14 Verify upload-to-review workflow, arbitrary uploads, failure recovery, persistence, row alignment and keyboard use. Depends on T11–T13.

## Phase 3 RAG and reranking

- [x] T15 Implement canonical serialization, LangChain Documents and reversible field/evidence span mapping. Depends on T12.
- [x] T16 Implement fixed-size chunking using a LangChain token splitter with pinned tokenizer and recorded parameters. Depends on T15.
- [x] T17 Implement logical semantic chunking with intact rows and bounded group splitting. Depends on T15.
- [ ] T18 Add a shared LangChain embedding adapter and PineconeVectorStore integration: namespaces, server-derived claim/revision filters, deterministic upserts, readiness checks and deletion. Keep a labeled local exact-search adapter for offline use. Verify network failures and visibility delays. Depends on T16–T17.
- [x] T19 Add cross-encoder reranking with original/final ranks, truncation metadata, timing and explicit failure states. Depends on T18.
- [x] T20 Implement a LangGraph question workflow with LangChain answer adapter, optional reranking, abstention, arithmetic support and citation validation; label lookup-only mode accurately. Depends on T19 and R3.
- [x] T21 Build assistant drawer with source navigation and retrieval configuration details. Depends on T11 and T20.
- [x] T22 Verify claim isolation, stale-index prevention, source grounding and resistance to instructions inside documents. Depends on T21.

## Phase 4 Evaluation and reports

- [ ] T23 Author 60 queries and gold evidence/answers; split 15 development and 45 held-out queries by claim case; review labels. Depends on T05.
- [x] T24 Define duplicate relevance policy, unanswerable handling, equal-token comparison and hand-verified metric examples. Depends on T23.
- [ ] T25 Build four-condition Pinecone runner with frozen snapshots, ready-index checks, backend/namespace/model/package manifests, raw candidate rankings and stage timings. Keep offline results separate. Depends on T19 and T24.
- [x] T26 Finalize parameters using development cases; freeze settings before held-out runs. Depends on T25.
- [x] T27 Run held-out retrieval and deterministic lookup evaluation; calculate paired deltas and claim-grouped intervals. Repeated generated-answer evaluation is outside the current runner.
- [x] T28 Generate chunking comparison report, reranking impact analysis and JSON/CSV artifacts, including regressions. Depends on T27.
- [x] T29 Add UI report view with clear measured versus pending states. Depends on T28.
- [ ] T30 Verify reproducibility and document Replit setup, synthetic preview data, mock/live switching, backend reachability, public configuration, server-side secrets and local offline operation. Validate connected preview upload/render/save/citations. Depends on T14, T22 and T29.

## Phase 5 Real extraction extension

- [ ] X01 Local RapidOCR selected with no external document transfer; formal labeled-set accuracy targets remain future validation.
- [x] X02 Implement best-effort orientation/deskew, crop checks and invertible evidence transforms.
- [ ] X03 Printed OCR and form-specific mapping implemented; reliable handwriting and broader layout coverage remain future work.
- [x] X04 Flag OCR values for review, preserve corrections on retry, expose raw text/failures and allow manual verification.
- [ ] X05 Measure actual field accuracy, row alignment, source localization and abstention by degradation type; publish limitations. Depends on X04.

## Completion checklist

- [ ] Every accepted first-release criterion has evidence from a working workflow or recorded evaluation.
- [x] Synthetic extraction is visibly labeled and never substituted for arbitrary uploaded content.
- [x] Both retrieval strategies and reranking are implemented and evaluated on the same query snapshots.
- [x] Reports contain measured results with provenance, including inconclusive or negative outcomes.
- [x] Every authored file has fewer than 100 lines; any tool-required generated-file exception is documented.
- [x] Implementation started after user review; deployment remains separate.
