import time
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from .chunking import chunks
from .embeddings import embeddings
from ..config import setting


def store(strategy):
    if not setting("PINECONE_API_KEY") or not setting("PINECONE_INDEX_HOST"):
        raise ValueError("Set PINECONE_API_KEY and PINECONE_INDEX_HOST for connected mode")
    index = Pinecone(api_key=setting("PINECONE_API_KEY")).Index(
        host=setting("PINECONE_INDEX_HOST"))
    description = index.describe_index_stats()
    if description["dimension"] != 384:
        raise ValueError("This embedding configuration requires a 384-dimensional index")
    model = "minilm" if embeddings().mode == "sentence" else "hash"
    namespace = f"{setting('PINECONE_NAMESPACE', 'cms1450-demo')}-{model}-{strategy}"
    return index, PineconeVectorStore(index=index, embedding=embeddings(), namespace=namespace)


def index(claim, strategy):
    if claim["sample"] is None and setting("ALLOW_REMOTE_UPLOADS") != "true":
        raise ValueError("Remote indexing of arbitrary uploads is disabled")
    raw, vector_store = store(strategy)
    docs = chunks(claim, strategy)
    ids = [f"{claim['id']}:{claim['revision']}:{strategy}:{n}" for n in range(len(docs))]
    if not docs:
        return 0
    vector_store.add_documents(docs, ids=ids)
    for attempt in range(8):
        found = raw.fetch(ids=ids, namespace=vector_store.namespace)
        if len(found.vectors) == len(ids):
            probe = vector_store.similarity_search(docs[0].page_content, k=len(ids),
                                                  filter=scope(claim))
            if len(probe) == len(ids):
                return len(docs)
        time.sleep(min(0.25 * 2 ** attempt, 2))
    raise ValueError("Pinecone visibility timed out; retry indexing")


def scope(claim):
    return {"$and": [{"claim_id": {"$eq": claim["id"]}},
                      {"revision": {"$eq": claim["revision"]}}]}


def search(claim, strategy, query, limit=20):
    _, vector_store = store(strategy)
    hits = vector_store.similarity_search_with_score(query, k=limit, filter=scope(claim))
    return [{"document": doc, "score": float(score), "initial_rank": n + 1}
            for n, (doc, score) in enumerate(hits)]
