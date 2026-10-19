# CMS1450 Claim Review and RAG Specification

Status: Implementation authorized; see IMPLEMENTATION_STATUS.md for delivered behavior and remaining boundaries. Keep authored files below 100 lines.

## Goal and delivery scope

Build a CMS-1450 claim review application with the original form on the left and editable logical groups on the right. Add evidence-based question answering, a chunking comparison report and a reranking impact analysis.

Curated samples remain synthetic. Uploaded forms now run automatic local printed-text OCR with separate CMS-1450 and CMS-1500 schemas; see OCR.md. Handwriting accuracy is unverified. Processing means intake, correction, validation and review; payer submission, adjudication and public publishing are outside scope.

## Reference and logical groups

Use the [CMS form information](https://www.cms.gov/medicare/cms-forms/cms-forms/cms-forms-items/cms1196256), [Chapter 25 instructions](https://www.cms.gov/manuals/downloads/clm104c25.pdf) and [public reference PDF](https://www.reginfo.gov/public/do/DownloadDocument?objectID=83037001). Inspect the historical PDF before selecting its form page; record source, revision, checksum and download date. Verify reuse permissions; use a labeled synthetic layout if redistribution is restricted. Downloadable references are not submission-ready forms.

These are proposed application groups. A versioned registry must cover every locator and subfield, with one owning group per field.

| Group | Form locators | Structure |
| --- | --- | --- |
| Provider and claim identity | 1–5, 56–57 | Provider and claim identifiers |
| Patient demographics | 8–11 | Identity and demographics |
| Statement and admission | 6, 12–17 | Dates and encounter details |
| Conditions and occurrences | 18–29, 31–36 | Codes, dates and spans |
| Responsible party and values | 38–41 | Contacts and code/amount pairs |
| Service lines and charges | 42–48 | Persistent row IDs; separate totals |
| Payers and coverage | 50–55, 58–65 | Preserve primary/secondary/tertiary associations |
| Diagnoses and procedures | 66–74 | Ordering, qualifiers and code/date pairs |
| Clinical providers | 76–79 | Provider identities and roles |
| Remarks and additional codes | 80–81 | Narrative and qualified codes |
| Reserved or unlabeled | 7, 30, 37, 49, 75 | Preserve unexpected content for review |

## Review interface

- Build React/TypeScript with Vite and PDF.js in Replit; keep portable source in `frontend/` and support local runs.
- Start with a typed mock API and matching synthetic fixtures; label mock and connected modes explicitly.
- Accept PDF, PNG and JPEG; proposed limits: 20 MB and 9 pages. Reject corrupt, encrypted and unsupported inputs.
- Match curated extractions by fixture checksum. Unmatched uploads show their pages and empty editable groups labeled extraction unavailable; never substitute unrelated dummy values.
- Provide a resizable 50/50 desktop view, page selection, zoom, rotation, group navigation, editable tables, validation and review counts. Small screens use source/fields tabs.
- Field selection opens and highlights its evidence; source selection focuses its field. Show unavailable locations explicitly. Support keyboard navigation and labeled controls.
- Save corrections, preserve original extraction, reopen work, handle revision conflicts and expose unsaved/save-failed states. Export reviewed JSON and audit history.
- Require resolution or reasoned acknowledgment of blocking issues before marking reviewed. Review does not imply payer acceptance.
- Put questions in an assistant drawer; citations open the relevant field, row or page. Display revision and retrieval configuration.

## Extraction and data contracts

Extraction creates structured evidence; RAG retrieves it. Keep both responsibilities separate. First implement a deterministic fixture adapter. Later add orientation detection, deskew, quality checks, printed OCR, handwriting recognition and layout-aware mapping using labels, neighboring text and relative positions; boundary lines are optional signals.

Keep original pages and invertible transforms. Evidence polygons use documented original-page coordinates. Unreadable, ambiguous or missing content produces nulls/review flags, not guesses. Store alternatives separately; raw provider scores are not calibrated probabilities. Simulated extraction cannot establish OCR accuracy.

Store document checksums and extraction mode; stable field/locator/group/row IDs; raw, normalized, extracted and edited values; evidence references; confidence source and review status. Distinguish missing, blank, unreadable and not applicable. Preserve leading zeros and use decimal currency.

Keep immutable claim revisions and audit events with actor, timestamp, changes and reason. Manual values without image evidence cite the reviewer. Chunks retain field/evidence IDs and source spans. Saving edits rebuilds affected indexes; answers require matching claim/index revisions. General logs omit claim text and patient identifiers.

## Architecture and integration

Use FastAPI, typed schemas, SQLite metadata and private backend file storage. LangGraph orchestrates ingestion and questions; LangChain supplies Documents, embedding/model interfaces, retrievers and prompts; Pinecone is the primary vector database.

The ingestion graph validates, renders, extracts, validates fields, interrupts for review, serializes, chunks, embeds and indexes. Use persistent SQLite checkpoints, stable thread IDs, revision checks and idempotent operations. Claim revisions remain authoritative. The question graph authorizes scope, checks readiness, retrieves, optionally reranks, answers/abstains and validates citations.

Use `langchain-pinecone` with server-side credentials, configured embedding dimension/metric, workspace/strategy namespaces, mandatory claim/revision filters and deterministic vector IDs. Authorization is enforced independently of namespaces. Verify record visibility before marking a revision ready; bound retries and expose failures. Keep immutable benchmark snapshots and candidate lists for replay.

Replit connects through a public API base URL to a reachable HTTPS backend or supported development proxy; configure explicit CORS origins. Backend hosting remains to be chosen. Keep secrets out of browser builds and external tracing off. Only synthetic fixtures enter connected Pinecone/Replit demos; arbitrary uploads remain on the backend unless remote indexing is explicitly enabled. Local storage means backend-host storage; browser uploads leave the device.

Retain a labeled local exact-search adapter and lookup-only answer mode for credential-free development. Never silently replace a failed live API or Pinecone benchmark with mocks/local results. Pin compatible versions during implementation. See [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [Pinecone integration](https://docs.langchain.com/oss/python/integrations/vectorstores/pinecone) and [Replit Secrets](https://replit.com/help/answers/what-is-the-best-way-to-store-api-keys-securely-in-replit).

## Retrieval and experiment

Both chunkers consume the same ordered, labeled serialization and evidence. Fixed chunks use 400 tokens with 60-token overlap and a pinned tokenizer. Semantic chunks follow the groups above, splitting oversized groups at row/field boundaries toward 400 tokens while preserving associations. Record indivisible oversized units. Neither strategy crosses claims or documents.

Use identical embeddings and Pinecone settings; retrieve 20 candidates and return 5, or fewer for small indexes. A local cross-encoder reranks the same candidates; record original/final ranks, truncation, timing and failures. Answers use retrieved evidence, citations and deterministic arithmetic; abstain on missing/conflicting evidence. Treat document instructions as data. Do not infer coverage or medical necessity from charges.

Curate 12 synthetic cases and 60 queries: 15 development and 45 held-out, split by claim case. Include lookups, dates, rows, multi-group reasoning, ambiguity and unanswerable questions. Independently review expected answers and graded field/evidence relevance; judgments must not depend on chunker outputs.

Compare fixed, fixed plus reranking, semantic and semantic plus reranking on identical snapshots. Freeze models, prompts, budgets and settings before held-out runs. Repeat nondeterministic answers three times; record seeds where supported and separate cold-start costs. Keep offline evaluations separate.

Report evidence Recall@5, MRR@5, nDCG@5 with explicit duplicate handling, context tokens and recall under an equal token budget. Exclude unanswerable queries from positive-relevance metrics and report abstention separately. Measure correctness, citation support, unsupported claims and stage latency; publish per-query values, paired deltas and claim-grouped bootstrap intervals. The small synthetic study does not establish production accuracy. Publish both reports and raw JSON/CSV, including negative/inconclusive effects.

## Acceptance and review gate

Accept the first release when upload/render/edit/save/reopen/export works; all locators and repeated rows are preserved; evidence navigation is accurate; structural date/format/total checks work; job recovery, revision conflicts and stale-index prevention work; claim isolation and document-instruction handling are verified; and all four experiments produce traceable measured reports.

Review scope, groups, Replit/backend connectivity, answer model and payer-specific rules before implementation. Real extraction requires separately labeled degraded images and agreed field accuracy, row alignment, localization and abstention targets. Production controls, real regulated data and deployment are separate scope. SEC filings and other financial-document adapters are future extensions.
