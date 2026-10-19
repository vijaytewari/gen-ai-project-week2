from functools import lru_cache
from langchain_core.embeddings import Embeddings
from sklearn.feature_extraction.text import HashingVectorizer
from ..config import setting

MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"


class LocalEmbeddings(Embeddings):
    def __init__(self):
        self.mode = setting("EMBEDDING_MODE", "hash")
        self.name = "hash-word-384-v1"
        self.revision = "v1"
        if self.mode == "sentence":
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                             revision=MODEL_REVISION)
            self.name = "sentence-transformers/all-MiniLM-L6-v2"
            self.revision = MODEL_REVISION
        elif self.mode == "hash":
            self.model = HashingVectorizer(n_features=384, alternate_sign=False,
                                           ngram_range=(1, 2), norm="l2")
        else:
            raise ValueError("EMBEDDING_MODE must be hash or sentence")

    def embed_documents(self, texts):
        if self.mode == "sentence":
            return self.model.encode(texts, normalize_embeddings=True).tolist()
        return self.model.transform(texts).toarray().tolist()

    def embed_query(self, text):
        return self.embed_documents([text])[0]


@lru_cache(maxsize=1)
def embeddings():
    return LocalEmbeddings()
