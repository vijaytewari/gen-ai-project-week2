# Chunking comparison

Run: 20261018T223339855865

Backend: local; embedding: hash-word-384-v1; reranker: lexical.

45 held-out queries from 9 synthetic cases; 15 development queries are excluded.
Gold labels are template-authored and not independently reviewed; results are provisional.
Unanswerable queries are excluded from positive-relevance metrics.
Novel-evidence nDCG uses linear gain and an ideal first result covering all gold fields.
Equal-token recall uses an 800-token budget over the top five whole chunks.

| Configuration | Recall@5 | MRR@5 | nDCG@5 | Recall/800 tokens | Answer accuracy | ms/query |
| --- | --- | --- | --- | --- | --- | --- |
| fixed | 1.000 | 0.958 | 0.969 | 1.000 | 0.933 | 5.71 |
| fixed-rerank | 1.000 | 1.000 | 1.000 | 1.000 | 0.933 | 4.30 |
| semantic | 1.000 | 0.903 | 0.928 | 1.000 | 0.933 | 7.67 |
| semantic-rerank | 1.000 | 1.000 | 1.000 | 1.000 | 0.933 | 6.82 |

Metrics CSV and per-query candidate/citation artifacts accompany each configuration.
Timings exclude embedding/index/model cold start. Lookup-mode accuracy measures field lookup, not generative reasoning.
Synthetic results do not establish real OCR, clinical, payer or production accuracy.
