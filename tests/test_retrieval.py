import time
from backend.app.rag.chunking import chunks
from backend.app.rag.serialization import canonical
from backend.app.rag.store import index_claim, retrieve
from backend.app.rag.reranking import rerank
from backend.app.claims import sample
from evaluation.metrics import retrieval_metrics, paired_interval


def test_chunk_boundaries_and_candidate_preservation(client):
    claim = sample(0)
    source = canonical(claim)
    for strategy in ("fixed", "semantic"):
        pieces = chunks(claim, strategy)
        assert pieces
        for piece in pieces:
            metadata = piece.metadata
            assert source.page_content[metadata["start"]:metadata["end"]] == piece.page_content
            assert metadata["claim_id"] == claim["id"]
        if strategy == "semantic":
            services = [d for d in pieces if "[services]" in d.page_content]
            assert all(f"47.{row}" in str([d.metadata for d in services]) for row in (1, 2))
    index_claim(claim)
    hits = retrieve(claim, "semantic", "What is the patient name?")
    ranked = rerank("What is the patient name?", hits)
    assert {h["document"].metadata["chunk_id"] for h in hits} == {
        h["document"].metadata["chunk_id"] for h in ranked}
    assert all(h["document"].metadata["claim_id"] == claim["id"] for h in ranked)


def test_review_index_question_and_stale_revision(client):
    claim = client.post("/api/samples/0").json()
    base = f"/api/claims/{claim['id']}"
    question = {"revision": 1, "query": "What is the patient name?", "strategy": "semantic", "rerank": True}
    assert client.post(base + "/questions", json=question).status_code == 409
    client.post(base + "/index")
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        status = client.get(base).json()["job"]
        if status["status"] in ("ready:1", "failed"):
            break
        time.sleep(.05)
    assert status["status"] == "ready:1", status
    answer = client.post(base + "/questions", json=question).json()
    assert any(c["field_id"] == "8" for c in answer["citations"])
    question["query"] = "What is the patient's bank account number?"
    assert client.post(base + "/questions", json=question).json()["abstained"]
    client.put(base + "/fields", json={"revision": 1, "changes": [{"field_id": "8", "value": "New Name"}]})
    assert client.post(base + "/questions", json=question).status_code == 409


def test_metrics_duplicate_evidence_and_pairing():
    from langchain_core.documents import Document
    def hit(keys):
        return {"document": Document(page_content="x", metadata={"field_ids": keys, "tokens": 10})}
    scores = retrieval_metrics([hit(["a"]), hit(["a"]), hit(["b"])], ["a", "b"])
    assert scores["recall"] == 1 and scores["mrr"] == 1
    assert scores["ndcg"] == .75
    assert retrieval_metrics([], ["a"])["recall"] == 0
    assert retrieval_metrics([], [])["recall"] is None
    left = [{"query_id": "q", "case": 1, "recall": 0}]
    right = [{"query_id": "q", "case": 1, "recall": 1}]
    assert paired_interval(left, right) == {"delta": 1, "low": 1, "high": 1}
