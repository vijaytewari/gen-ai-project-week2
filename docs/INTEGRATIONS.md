# Models and vector storage

## Lightweight baseline

The default uses the same 384-dimensional hashing embedding function for all configurations,
local exact similarity search, explicit lexical reranking and deterministic evidence lookup.
This provides a runnable review and evaluation workflow without cloud accounts.

## Neural retrieval and reranking

Install CPU PyTorch first to avoid downloading GPU runtime dependencies:

```sh
pip install torch==2.7.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements-models.txt
python -m scripts.warm_models
```

Set these values in `.env`, then restart the backend and reindex:

```text
EMBEDDING_MODE=sentence
RERANKER=cross-encoder
```

Models: `sentence-transformers/all-MiniLM-L6-v2` and `cross-encoder/ms-marco-MiniLM-L-6-v2`.
Model caches live in `data/models/`; initialization fails explicitly if unavailable. No automatic heuristic fallback occurs.
The warmup script validates embedding dimensions and a reranking inference. Model downloads require internet.

## Pinecone

Create a cosine index with 384 dimensions in your chosen Pinecone account/region.
This project connects to an existing index; it does not automatically provision paid resources.

```text
VECTOR_BACKEND=pinecone
PINECONE_API_KEY=your-server-key
PINECONE_INDEX_HOST=your-index-host
PINECONE_NAMESPACE=cms1450-demo
EMBEDDING_MODE=sentence
```

Strategies use separate namespaces. Server-derived claim/revision filters restrict every query.
Deterministic IDs support retry-safe writes; readiness requires visibility checks. Network failures are explicit.
Remote arbitrary-upload indexing is disabled by default. Do not enable it for real patient data in this prototype.
Pinecone mode requires real credentials; local tests do not establish live Pinecone connectivity.
Use a new namespace when changing embedding models; equal dimensions do not make different embeddings interchangeable.

## Optional generated answers

With optional model dependencies installed, set `ANSWER_MODE=llm`, `OPENAI_API_KEY` and `OPENAI_MODEL`.
The default configurable model name is `gpt-4.1-mini`; choose one available to your account.
The adapter uses structured output and validates citation IDs. Review answer support manually;
citation validity alone cannot prove every generated statement is supported.
The included benchmark deliberately evaluates deterministic lookup answers only.

## Experiment execution

Run `python -m evaluation.run` after selecting one backend/model configuration.
Run `python -m scripts.benchmark_neural` to reproduce the included local neural experiment after model warmup.
All four chunking/reranking conditions share that configuration. Separate runs compare baseline and neural modes.
Reports include raw candidate ranks, field citations, metric CSVs, model/package manifests and paired intervals.
Judgments are template-authored, not independently validated; results remain provisional.
