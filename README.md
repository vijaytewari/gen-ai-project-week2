# Claims Processor

A Replit-ready React UI and FastAPI backend for reviewing synthetic institutional claims.
Upload a form, press Analyzer for OCR/schema generation, review source-linked fields, then save JSON.
LangGraph coordinates review/indexing and questions; LangChain provides the RAG interfaces; Pinecone is optional connected storage.

## Run locally

Requires Python 3.11+ and Node 22.16+. This workspace also has `.venv/` and a private Node runtime in `.runtime/`.

```sh
python -m venv .venv
# Activate your virtual environment before these commands.
pip install -r requirements.txt
cd frontend
npm ci
npm run build
cd ..
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. For frontend development, run `npm run dev` inside `frontend/`; Vite proxies `/api` to port 8000.
In this prepared Windows workspace, `powershell -File scripts/start.ps1` starts the already-built app.
Copy `.env.example` to `.env` for configuration. Model and Pinecone keys belong on the server.

## Replit

Import this repository into a Python/Node Replit environment and use Run (`scripts/replit.sh`).
The script installs dependencies, builds the UI and serves UI/API together on port 8000, avoiding cross-origin configuration.
See [the Replit build brief](docs/REPLIT_BUILD_BRIEF.md) for UI handoff and a separately hosted backend.
No project has been created or published to Replit from this workspace.

## Review workflow

1. Open **Review by HITL**, upload PDF/PNG/JPEG, then press **Analyzer**. Upload alone does not run OCR.
2. Select a field to highlight its source. Use **Save fields** or **Save & mark reviewed** to store corrections.
3. Select **Index current draft**, wait for readiness, then open **Ask this claim**.
4. Use **View JSON** or **Download JSON** in the workspace or library. JSON includes blank fields, original values, revisions and audit events.
5. Open **Retrieval insights** to run or inspect a measured four-configuration comparison.

The library contains only explicitly saved JSON, with one record per claim. Uploads and Analyzer results remain drafts.
Saving updates `data/json/<claim-id>.json`; SQLite retains the complete revision/edit history and published JSON.
Exports include `form_schema`, its corresponding `form_data`, and a local `schema_validation` report.
Twelve synthetic fixtures remain available to tests and evaluation, with simulated extraction. Other uploads use real local OCR.
Set server-side `OPENAI_API_KEY` and `OPENAI_SCHEMA_MODEL` for GPT schema generation; see [Analyzer setup](docs/ANALYZER.md).
Unknown forms retain raw text for manual review. See [OCR behavior](docs/OCR.md).
The public reference was downloaded separately and its provenance is in `fixtures/reference_manifest.json`.

## Retrieval modes and reports

Default mode is local hashed embeddings, exact vector search, lexical reranking and deterministic field lookup.
These are labeled baseline modes, not neural embeddings or generated answers. Run `python -m evaluation.run` to reproduce reports.
See [model and Pinecone setup](docs/INTEGRATIONS.md) for real MiniLM embeddings, cross-encoder reranking and optional LLM answers.
Generated experiment reports live in `reports/<run-id>/`; judgments are template-authored and provisional.

## Verification and file size

```sh
python -m pytest -q
python scripts/check_lines.py
cd frontend
npm run build
npx playwright test
```

Browser tests start an isolated app on port 8001 with separate data; they never populate your port-8000 library.
Microsoft Edge is required locally. Adjust `playwright.config.ts` for another browser.
Every authored code/document/result file is below 100 lines. The generated npm lockfile, dependency trees,
runtime caches and minified build outputs are excluded from that source-file rule.
Local printed-text OCR is implemented; reliable handwriting extraction and regulated production deployment remain separate milestones.
