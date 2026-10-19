import math
import random
from statistics import mean


def retrieval_metrics(hits, gold, budget=800):
    gold = set(gold)
    if not gold:
        return {"recall": None, "mrr": None, "ndcg": None, "recall_budget": None}
    seen, dcg, reciprocal, budget_seen, used = set(), 0.0, 0.0, set(), 0
    for rank, hit in enumerate(hits[:5], 1):
        metadata = hit["document"].metadata
        relevant = set(metadata["field_ids"]) & gold
        novel = relevant - seen
        if relevant and not reciprocal:
            reciprocal = 1 / rank
        dcg += len(novel) / math.log2(rank + 1)
        seen |= relevant
        if used + metadata["tokens"] <= budget:
            budget_seen |= relevant
            used += metadata["tokens"]
    return {"recall": len(seen) / len(gold), "mrr": reciprocal,
            "ndcg": dcg / len(gold), "recall_budget": len(budget_seen) / len(gold)}


def aggregate(rows):
    metrics = ["recall", "mrr", "ndcg", "recall_budget", "answer_accuracy",
               "latency_ms", "context_tokens", "citation_support", "unsupported_rate"]
    result = {key: mean(r[key] for r in rows if r[key] is not None) for key in metrics}
    negatives = [r for r in rows if not r["gold"]]
    result["abstention_accuracy"] = mean(r["abstained"] for r in negatives) if negatives else 0
    return result


def paired_interval(before, after, metric="recall", repeats=1000):
    groups = {}
    for left, right in zip(before, after):
        if left["query_id"] != right["query_id"]:
            raise ValueError("Paired queries must match")
        if left[metric] is not None:
            groups.setdefault(left["case"], []).append(right[metric] - left[metric])
    values = [mean(group) for group in groups.values()]
    rng = random.Random(2026)
    draws = sorted(mean(rng.choices(values, k=len(values))) for _ in range(repeats))
    return {"delta": mean(values), "low": draws[int(repeats * .025)],
            "high": draws[int(repeats * .975)]}
