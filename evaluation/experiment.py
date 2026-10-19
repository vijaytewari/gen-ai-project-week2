import time
from backend.app.rag.store import retrieve
from backend.app.rag.reranking import rerank
from backend.app.rag.answering import answer
from .metrics import retrieval_metrics


def evaluate(claim, query, strategy, enabled, cache):
    start = time.perf_counter()
    key = (query["id"], strategy)
    if key not in cache:
        candidates = retrieve(claim, strategy, query["query"])
        cache[key] = (candidates, (time.perf_counter() - start) * 1000)
    candidates, retrieval_ms = cache[key]
    retrieved = time.perf_counter()
    hits = rerank(query["query"], candidates) if enabled and candidates else candidates
    ranked = time.perf_counter()
    chosen = hits[:5]
    response = answer(claim, query["query"], chosen)
    ended = time.perf_counter()
    cited = {c["field_id"]: c["value"] for c in response["citations"]}
    expected = query["expected"]
    correct = (all(cited.get(key) == value for key, value in expected.items())
               and not response["abstained"]) if expected else response["abstained"]
    allowed = {key for h in chosen for key in h["document"].metadata["field_ids"]}
    supported = all(c["field_id"] in allowed for c in response["citations"])
    row = {"query_id": query["id"], "case": query["case"], "category": query["category"],
           "gold": query["gold"], **retrieval_metrics(chosen, query["gold"]),
           "answer_accuracy": int(correct), "citation_support": int(supported),
           "unsupported_rate": int(not supported), "abstained": response["abstained"],
           "latency_ms": retrieval_ms + (ended - retrieved) * 1000,
           "retrieval_ms": retrieval_ms,
           "reranking_ms": (ranked - retrieved) * 1000,
           "answer_ms": (ended - ranked) * 1000,
           "context_tokens": sum(h["document"].metadata["tokens"] for h in chosen)}
    evidence = {"query": query, "answer": response, "candidates": [
        {"chunk_id": h["document"].metadata["chunk_id"], "field_ids": h["document"].metadata["field_ids"],
         "score": h["score"], "initial_rank": h["initial_rank"], "rerank_score": h.get("rerank_score")}
        for h in hits]}
    return row, evidence
