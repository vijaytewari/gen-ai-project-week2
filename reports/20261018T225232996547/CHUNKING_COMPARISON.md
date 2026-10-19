# Chunking comparison

Run: 20261018T225232996547

Backend: local; embedding: sentence-transformers/all-MiniLM-L6-v2; reranker: cross-encoder.

45 held-out queries from 9 synthetic cases; 15 development queries are excluded.
Gold labels are template-authored and not independently reviewed; results are provisional.
Unanswerable queries are excluded from positive-relevance metrics.
Novel-evidence nDCG uses linear gain and an ideal first result covering all gold fields.
Equal-token recall uses an 800-token budget over the top five whole chunks.

| Configuration | Recall@5 | MRR@5 | nDCG@5 | Recall/800 tokens | Answer accuracy | ms/query |
| --- | --- | --- | --- | --- | --- | --- |
| fixed | 1.000 | 0.694 | 0.774 | 1.000 | 1.000 | 31.47 |
| fixed-rerank | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 890.10 |
| semantic | 1.000 | 0.875 | 0.908 | 1.000 | 1.000 | 70.02 |
| semantic-rerank | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1250.82 |

Metrics CSV and per-query candidate/citation artifacts accompany each configuration.
Timings exclude embedding/index/model cold start. Lookup-mode accuracy measures field lookup, not generative reasoning.
Each strategy reuses its baseline candidate list and retrieval timing for the reranking condition.
Synthetic results do not establish real OCR, clinical, payer or production accuracy.
