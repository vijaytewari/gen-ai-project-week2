# Measured experiments

The UI lists completed runs by date. Each run contains a chunking comparison, reranking impact report,
configuration manifest, per-configuration CSVs and per-query candidate/citation artifacts.

Initial lightweight baseline: `20261018T223339855865` (hash embeddings and lexical reranking).
Initial neural run: `20261018T224341205909` (MiniLM embeddings and cross-encoder reranking).
Paired-candidate neural run: `20261018T224742230859` (pinned revisions, shared candidates).
Final source-verified neural run: `20261018T225232996547` (corrected PDF text and continuation pages).

Use the final source-verified run for interpretation. Earlier runs preserve development history.
Reports measure local exact retrieval. Pinecone execution requires credentials and has not been run here.

The synthetic held-out set contains 45 questions across nine claims; 15 development queries are excluded.
Gold labels are template-authored and provisional. Answer accuracy refers to field lookup, not generative reasoning.
Perfect Recall@5 on this small corpus does not establish production retrieval quality.
The reranking report also measures MRR and nDCG, which can improve when recall is unchanged.

Reproduce with `python -m evaluation.run` after selecting backend and model modes in `.env`.
