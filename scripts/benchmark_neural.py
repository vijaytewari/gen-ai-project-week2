"""Reproduce the local neural run after `python -m scripts.warm_models`."""
import os
os.environ["VECTOR_BACKEND"] = "local"
os.environ["EMBEDDING_MODE"] = "sentence"
os.environ["RERANKER"] = "cross-encoder"
os.environ["ANSWER_MODE"] = "lookup"
os.environ["HF_HUB_OFFLINE"] = "1"
from evaluation.run import run


if __name__ == "__main__":
    result = run()
    print(result["run_id"])
