# Reranking impact

Run: 20261018T223339855865

Paired query differences; 95% bootstrap intervals resample claim cases (seed 2026).

| Strategy | Recall delta | 95% interval | Relative recall change | Latency delta ms |
| --- | --- | --- | --- | --- |
| fixed | +0.000 | [+0.000, +0.000] | 0.0% | -1.41 |
| semantic | +0.000 | [+0.000, +0.000] | 0.0% | -0.85 |

Zero and negative changes are valid outcomes; reranking cannot recover missing candidates.
Lexical mode is a heuristic baseline; cross-encoder mode must be measured separately.
Small synthetic, template-derived judgments and field-only answers limit these findings.
