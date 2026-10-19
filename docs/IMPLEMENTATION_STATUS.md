# Implementation status

The user approved implementation on October 18, 2026. Every authored source file remains below 100 lines.

## Implemented

- React/TypeScript/Vite UI, Replit run configuration and same-origin FastAPI serving.
- CMS-1450 reference retrieval and provenance; an original synthetic claim layout avoids bundling the official form.
- Twelve fixtures, eleven logical groups, all 81 locator positions and prototype subfields.
- Upload/render, field/source selection, rotation/zoom, mobile tabs and service-line table with added rows.
- Saved revisions, original values, audit export, conflict detection, structural checks and review acknowledgments.
- Footer field saves, save-before-review, and formatted JSON viewing/download with saved values and audit history.
- Claims Processor branding, Review by HITL upload page, and uploaded-claim JSON library with no demo-document entries.
- Explicit-save-only JSON library, one file per saved claim in data/json, all defined fields and complete revision/edit history.
- Persistent LangGraph review/index checkpoints and question graph.
- LangChain Documents, token splitting, embedding interfaces and optional generated-answer adapter.
- Fixed/semantic chunkers, local exact search and Pinecone integration with server-derived scope filters.
- Local MiniLM embeddings and cross-encoder reranking, with separate lightweight baseline modes.
- Claim/revision index gating, evidence lookup, abstention and clickable citations.
- Four-condition evaluation, raw rankings, metrics CSVs, bootstrap intervals and comparison reports.
- Top-of-workspace Analyzer triggers local OCR, form detection, source highlights and GPT schema generation when configured.
- JSON Schema validation runs locally; missing GPT credentials/errors use a visibly labeled local schema fallback.
- Isolated browser-test server/data prevents test records from entering the user's library.

## Verified locally

Backend tests exercise persistence/conflicts, validation, fixture matching, unmatched uploads, chunk mappings,
candidate preservation, metric examples, service-line identity, revision gating and missing-credential behavior.
Headless Edge tests exercise desktop and mobile UI, PDF rendering, correction/reopen and citation navigation.
Editing/export checks cover edits after review, persisted JSON, downloads and retaining corrections on save conflicts.
Checkpoint recovery is tested by resuming human review in a separate Python process.
TypeScript compilation and production frontend build succeed. The file-size checker verifies authored files and result artifacts.
Actual MiniLM embedding and cross-encoder inference ran locally; measured neural reports accompany baseline results.

## Remaining boundaries

- Pinecone credentials were not provided: the adapter exists, but live upsert/query/network behavior is unverified.
- OpenAI credentials were not provided: GPT schema generation is tested with mocked responses, not a live call.
- Replit-ready source and run configuration exist; no Replit project or hosted deployment has been created.
- Curated samples remain simulated; other uploads now use real printed-text OCR. Handwriting accuracy remains unverified.
- The locator registry is complete at locator level; exhaustive UB-04 subfield/qualifier and payer-rule coverage is future work.
- The benchmark uses template-authored judgments; independent review and a broader query set remain future validation.
- Included answer benchmarks evaluate deterministic field lookup. Generated-answer correctness is not yet benchmarked.
- Lookup mode handles matching fields, not arbitrary clinical reasoning, coverage decisions or generalized financial documents.
- Production identity/access controls, retention, background-worker deployment and real patient-data handling need separate work.

Generated dependency lockfiles, binary PDFs and minified outputs are excluded from the authored-code line limit.
