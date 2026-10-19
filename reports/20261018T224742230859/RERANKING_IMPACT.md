# Reranking impact

Run: 20261018T224742230859

Paired query differences; 95% bootstrap intervals resample claim cases (seed 2026).

| Strategy | Recall delta | 95% interval | Relative recall change | Latency delta ms |
| --- | --- | --- | --- | --- |
| fixed | +0.000 | [+0.000, +0.000] | 0.0% | +733.99 |
| semantic | +0.000 | [+0.000, +0.000] | 0.0% | +1348.53 |

Zero and negative changes are valid outcomes; reranking cannot recover missing candidates.
Lexical mode is a heuristic baseline; cross-encoder mode must be measured separately.
Small synthetic, template-derived judgments and field-only answers limit these findings.

| Strategy | Rank metric | Paired delta | 95% interval |
| --- | --- | --- | --- |
| fixed | mrr | +0.306 | [+0.264, +0.347] |
| fixed | ndcg | +0.226 | [+0.195, +0.256] |
| fixed | answer_accuracy | +0.000 | [+0.000, +0.000] |
| semantic | mrr | +0.125 | [+0.125, +0.125] |
| semantic | ndcg | +0.092 | [+0.092, +0.092] |
| semantic | answer_accuracy | +0.000 | [+0.000, +0.000] |

Latency is a single ordered pass; caching can dominate small timing differences.
