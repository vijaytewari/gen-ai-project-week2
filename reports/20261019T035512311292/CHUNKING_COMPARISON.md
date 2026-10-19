# Chunking comparison

Run: 20261019T035512311292

Backend: local; embedding: hash-word-384-v1; reranker: lexical.

45 held-out queries from 9 synthetic cases; 15 development queries are excluded.
Gold labels are template-authored and not independently reviewed; results are provisional.
Unanswerable queries are excluded from positive-relevance metrics.
Novel-evidence nDCG uses linear gain and an ideal first result covering all gold fields.
Equal-token recall uses an 800-token budget over the top five whole chunks.

| Configuration | Recall@5 | MRR@5 | nDCG@5 | Recall/800 tokens | Answer accuracy | ms/query |
| --- | --- | --- | --- | --- | --- | --- |
| fixed | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 8.63 |
| fixed-rerank | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 9.51 |
| semantic | 1.000 | 0.986 | 0.990 | 1.000 | 1.000 | 9.97 |
| semantic-rerank | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 10.84 |

Metrics CSV and per-query candidate/citation artifacts accompany each configuration.
Timings exclude embedding/index/model cold start. Lookup-mode accuracy measures field lookup, not generative reasoning.
Each strategy reuses its baseline candidate list and retrieval timing for the reranking condition.
Synthetic results do not establish real OCR, clinical, payer or production accuracy.
