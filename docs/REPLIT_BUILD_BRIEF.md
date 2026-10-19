# Replit UI build brief

Build and preview the existing React/TypeScript/Vite frontend in Replit. Preserve the API contracts and under-100-line authored-file limit.

## Screens

- Document library: drag/drop upload, scenario badges, search and 12 synthetic claims.
- Claim workspace: resizable source/fields split, PDF.js zoom/rotation/pages and two-way field highlights.
- Field review: logical groups, repeated field row IDs, statuses, simulated confidence, original values and validation acknowledgments.
- Claim assistant: chunk strategy, reranking toggle, citations, timings, retrieved chunks and explicit unavailable/abstention states.
- Retrieval insights: measured four-condition results, report links and experiment progress/failure.

## Run together

The root `.replit` runs `scripts/replit.sh`, which installs dependencies and serves built frontend plus FastAPI on port 8000.
`replit.nix` requests Python 3.11 and Node 22; see [Replit configuration](https://docs.replit.com/features/project-setup/configuration).
Use a Python 3.11+ / Node 22.16+ environment. Keep `.env` local and credentials in Replit Secrets.
The review UI and local baseline require no paid model or Pinecone credentials; initial tokenizer setup requires internet.
Sentence embedding and cross-encoder models require optional model dependencies and downloads.

## Run against a separate backend

Set public `VITE_API_BASE_URL` before frontend build, for example `https://your-backend.example`.
Set backend `CORS_ORIGINS` to the exact Replit preview origin. Never embed provider keys in `VITE_*` variables.
The backend must be reachable over HTTPS; a remote Replit process cannot use a developer machine's localhost as its backend.

## API contracts

Types are in `frontend/src/types.ts`; request functions are in `frontend/src/api.ts`; backend schemas are in `backend/app/models.py`.
OpenAPI is served at `/docs`. Sample endpoints return real fixture-backed data, not placeholder scores.

```text
GET  /api/samples                     samples and group registry
POST /api/samples/{case}              new editable synthetic claim
POST /api/documents                   multipart file upload
GET  /api/claims/{id}                 revision, fields, issues and job status
GET  /api/claims/{id}/original         original PDF
PUT  /api/claims/{id}/fields           revision and changes
POST /api/claims/{id}/review           revision, group and acknowledgment
POST /api/claims/{id}/index            index current draft
POST /api/claims/{id}/questions        revision, query, strategy and rerank
GET  /api/claims/{id}/export           reviewed data and audit
GET  /api/reports                     measured experiment summaries
POST /api/reports/run                 queue a comparison
```

## Review acceptance

Keep source and editable values visible together on desktop, with source/fields tabs on phones.
Run local OCR for uploads; show progress, detected schema, raw text and review flags. Never substitute dummy extraction.
Disable questions while unsaved or unindexed. Preserve conflicts and API errors; do not silently use mock data on failures.
Use synthetic documents only in this preview. Publishing remains a separate action; no Replit publication is performed here.
