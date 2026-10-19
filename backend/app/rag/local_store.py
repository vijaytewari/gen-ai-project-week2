import json
import numpy as np
from langchain_core.documents import Document
from .chunking import chunks
from .embeddings import embeddings
from ..config import DATA


def cache_path(claim, strategy):
    path = DATA / "indexes"
    path.mkdir(exist_ok=True)
    return path / f"{claim['id']}-{claim['revision']}-{strategy}.json"


def index(claim, strategy):
    docs = chunks(claim, strategy)
    vectors = embeddings().embed_documents([d.page_content for d in docs]) if docs else []
    data = {"embedding": embeddings().name, "embedding_revision": embeddings().revision,
            "documents": [d.model_dump() for d in docs],
            "vectors": vectors}
    target = cache_path(claim, strategy)
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(data), encoding="utf-8")
    temporary.replace(target)
    return len(docs)


def search(claim, strategy, query, limit=20):
    path = cache_path(claim, strategy)
    if not path.exists():
        raise ValueError("Current revision is not indexed")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["embedding"] != embeddings().name:
        raise ValueError("Embedding model changed; reindex this claim")
    if data.get("embedding_revision") != embeddings().revision:
        raise ValueError("Embedding revision changed; reindex this claim")
    if not data["documents"]:
        return []
    scores = np.array(data["vectors"]) @ np.array(embeddings().embed_query(query))
    order = np.argsort(-scores, kind="stable")[:limit]
    return [{"document": Document(**data["documents"][i]), "score": float(scores[i]),
             "initial_rank": rank + 1} for rank, i in enumerate(order)]
