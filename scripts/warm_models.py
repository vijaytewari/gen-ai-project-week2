"""Download and smoke-test the optional local neural models."""
import os
os.environ["EMBEDDING_MODE"] = "sentence"
os.environ["RERANKER"] = "cross-encoder"
from backend.app.rag.embeddings import embeddings
from backend.app.rag.reranking import cross_encoder


if __name__ == "__main__":
    vector = embeddings().embed_query("What are the claim charges?")
    score = cross_encoder().predict([("claim charges", "Total charges: 1450.00")])
    print(f"Embedding dimensions: {len(vector)}; cross-encoder score: {score[0]:.4f}")
