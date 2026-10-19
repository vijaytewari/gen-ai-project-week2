import re
from functools import lru_cache
from ..config import setting

MODEL_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"


@lru_cache(maxsize=1)
def cross_encoder():
    from sentence_transformers import CrossEncoder
    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", max_length=512,
                        revision=MODEL_REVISION)


def rerank(query, hits):
    mode = setting("RERANKER", "lexical")
    if mode == "cross-encoder":
        scores = cross_encoder().predict([(query, h["document"].page_content) for h in hits])
    elif mode == "lexical":
        terms = set(re.findall(r"[a-z0-9]+", query.lower())) - {"what", "is", "the", "for", "this"}
        scores = []
        for hit in hits:
            lines = hit["document"].page_content.lower().splitlines()
            coverage = [len(terms & set(re.findall(r"[a-z0-9]+", line))) / max(len(terms), 1)
                        for line in lines]
            scores.append(max(coverage, default=0) + hit["score"] * 0.01)
    else:
        raise ValueError("RERANKER must be lexical or cross-encoder")
    ranked = [{**hit, "rerank_score": float(score)} for hit, score in zip(hits, scores)]
    return sorted(ranked, key=lambda h: -h["rerank_score"])
