from .metrics import paired_interval


def reports(folder, summary, rows):
    header = ["# Chunking comparison", "", f"Run: {summary['run_id']}", "",
        f"Backend: {summary['backend']}; embedding: {summary['embedding']}; reranker: {summary['reranker']}.",
        "", "45 held-out queries from 9 synthetic cases; 15 development queries are excluded.",
        "Gold labels are template-authored and not independently reviewed; results are provisional.",
        "Unanswerable queries are excluded from positive-relevance metrics.",
        "Novel-evidence nDCG uses linear gain and an ideal first result covering all gold fields.",
        "Equal-token recall uses an 800-token budget over the top five whole chunks.",
        "", "| Configuration | Recall@5 | MRR@5 | nDCG@5 | Recall/800 tokens | Answer accuracy | ms/query |",
        "| --- | --- | --- | --- | --- | --- | --- |"]
    for config in summary["configs"]:
        header.append(f"| {config['name']} | {config['recall']:.3f} | {config['mrr']:.3f} | "
            f"{config['ndcg']:.3f} | {config['recall_budget']:.3f} | "
            f"{config['answer_accuracy']:.3f} | {config['latency_ms']:.2f} |")
    header += ["", "Metrics CSV and per-query candidate/citation artifacts accompany each configuration.",
        "Timings exclude embedding/index/model cold start. Lookup-mode accuracy measures field lookup, not generative reasoning.",
        "Each strategy reuses its baseline candidate list and retrieval timing for the reranking condition.",
        "Synthetic results do not establish real OCR, clinical, payer or production accuracy."]
    (folder / "CHUNKING_COMPARISON.md").write_text("\n".join(header) + "\n", encoding="utf-8")
    impact = ["# Reranking impact", "", f"Run: {summary['run_id']}", "",
        "Paired query differences; 95% bootstrap intervals resample claim cases (seed 2026).", "",
        "| Strategy | Recall delta | 95% interval | Relative recall change | Latency delta ms |",
        "| --- | --- | --- | --- | --- |"]
    for strategy in ("fixed", "semantic"):
        left, right = rows[strategy], rows[f"{strategy}-rerank"]
        interval = paired_interval(left, right)
        before = next(c for c in summary["configs"] if c["name"] == strategy)
        after = next(c for c in summary["configs"] if c["name"] == f"{strategy}-rerank")
        relative = f"{interval['delta'] / before['recall']:.1%}" if before["recall"] else "undefined"
        impact.append(f"| {strategy} | {interval['delta']:+.3f} | [{interval['low']:+.3f}, "
            f"{interval['high']:+.3f}] | {relative} | {after['latency_ms'] - before['latency_ms']:+.2f} |")
    impact += ["", "Zero and negative changes are valid outcomes; reranking cannot recover missing candidates.",
        "Lexical mode is a heuristic baseline; cross-encoder mode must be measured separately.",
        "Small synthetic, template-derived judgments and field-only answers limit these findings."]
    impact += ["", "| Strategy | Rank metric | Paired delta | 95% interval |",
               "| --- | --- | --- | --- |"]
    for strategy in ("fixed", "semantic"):
        for metric in ("mrr", "ndcg", "answer_accuracy"):
            delta = paired_interval(rows[strategy], rows[f"{strategy}-rerank"], metric)
            impact.append(f"| {strategy} | {metric} | {delta['delta']:+.3f} | "
                          f"[{delta['low']:+.3f}, {delta['high']:+.3f}] |")
    impact += ["", "Latency is a single ordered pass; caching can dominate small timing differences."]
    (folder / "RERANKING_IMPACT.md").write_text("\n".join(impact) + "\n", encoding="utf-8")
