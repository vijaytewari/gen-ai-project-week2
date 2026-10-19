import pytest
from fastapi import HTTPException
from backend.app.rag import pinecone_store
from backend.app.claims import sample


def test_pinecone_filter_is_derived_from_claim_and_revision(client):
    claim = sample(0)
    scope = pinecone_store.scope(claim)
    assert scope == {"$and": [{"claim_id": {"$eq": claim["id"]}},
                               {"revision": {"$eq": 1}}]}


def test_pinecone_does_not_fall_back_when_credentials_missing(monkeypatch):
    monkeypatch.delenv("PINECONE_API_KEY", raising=False)
    monkeypatch.delenv("PINECONE_INDEX_HOST", raising=False)
    with pytest.raises(ValueError, match="PINECONE_API_KEY"):
        pinecone_store.store("semantic")


def test_unknown_claim_is_not_a_cross_claim_search(client):
    response = client.post("/api/claims/not-a-real-claim/questions", json={
        "revision": 1, "query": "patient name", "strategy": "semantic", "rerank": False})
    assert response.status_code == 404


def test_matching_fixture_upload_preserves_extraction_mode(client):
    claim = client.post("/api/samples/0").json()
    payload = client.get(f"/api/claims/{claim['id']}/original").content
    uploaded = client.post("/api/documents", files={"file": ("renamed.pdf", payload)})
    assert uploaded.status_code == 200
    assert uploaded.json()["sample"] == 0
    assert uploaded.json()["mode"] == "curated"
