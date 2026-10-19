from ..config import setting


def adapter():
    backend = setting("VECTOR_BACKEND", "local")
    if backend == "pinecone":
        from . import pinecone_store
        return pinecone_store
    if backend == "local":
        from . import local_store
        return local_store
    raise ValueError("VECTOR_BACKEND must be local or pinecone")


def index_claim(claim):
    return {strategy: adapter().index(claim, strategy) for strategy in ("fixed", "semantic")}


def retrieve(claim, strategy, query):
    return adapter().search(claim, strategy, query)
