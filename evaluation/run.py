import argparse
import importlib.metadata
import time
from datetime import datetime, timezone
from backend.app import database as db
from backend.app.claims import sample
from backend.app.config import REPORTS, setting
from backend.app.rag.store import index_claim
from backend.app.rag.embeddings import embeddings
from backend.app.rag.reranking import MODEL_REVISION as RERANK_REVISION
from .dataset import queries
from .experiment import evaluate
from .metrics import aggregate
from .artifacts import write_json, write_rows, write_evidence
from .reporting import reports


def run():
    if setting("ANSWER_MODE", "lookup") != "lookup":
        raise ValueError("Benchmark currently supports deterministic lookup answers only")
    db.initialize()
    started = time.perf_counter()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    folder = REPORTS / run_id
    folder.mkdir()
    claims = {i: sample(i) for i in range(3, 12)}
    for claim in claims.values():
        index_claim(claim)
    cold = time.perf_counter() - started
    summary = {"run_id": run_id, "backend": setting("VECTOR_BACKEND", "local"),
        "embedding": embeddings().name, "reranker": setting("RERANKER", "lexical"),
        "query_count": 45, "cases": 9, "configs": []}
    manifest = {"run_id": run_id, "cold_start_seconds": cold, "seed": 2026,
        "chunk_tokens": 400, "overlap_tokens": 60, "candidates": 20, "top_k": 5,
        "namespace": setting("PINECONE_NAMESPACE", "cms1450-demo"),
        "models": {"embedding": embeddings().name, "embedding_revision": embeddings().revision,
                   "reranker": summary["reranker"], "reranker_revision": RERANK_REVISION},
        "candidate_reuse": True,
        "versions": {p: importlib.metadata.version(p) for p in
                     ["langgraph", "langchain-core", "langchain-pinecone", "tiktoken", "numpy"]},
        "claim_snapshots": [{"id": c["id"], "revision": c["revision"], "sha256": c["sha256"]}
                            for c in claims.values()], "label_review": "template-authored, provisional"}
    write_json(folder / "manifest.json", manifest)
    all_rows, cache = {}, {}
    for strategy in ("fixed", "semantic"):
        for enabled in (False, True):
            name = strategy + ("-rerank" if enabled else "")
            target = folder / name
            target.mkdir()
            rows = []
            for number, query in enumerate(q for q in queries() if q["split"] == "heldout"):
                row, evidence = evaluate(claims[query["case"]], query, strategy, enabled, cache)
                rows.append(row)
                write_evidence(target, number, evidence)
            all_rows[name] = rows
            write_rows(target / "metrics.csv", rows)
            summary["configs"].append({"name": name, "strategy": strategy,
                                       "rerank": enabled, **aggregate(rows)})
    write_json(folder / "summary.json", summary)
    reports(folder, summary, all_rows)
    return summary


if __name__ == "__main__":
    argparse.ArgumentParser(description="Run the held-out synthetic benchmark").parse_args()
    result = run()
    print(f"Completed {result['run_id']} ({result['backend']}, {result['reranker']})")
