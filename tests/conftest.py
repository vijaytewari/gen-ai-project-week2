import os
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

TEST_DATA = tempfile.TemporaryDirectory(prefix="claimlens-tests-")
os.environ["DATA_DIR"] = str(Path(TEST_DATA.name))
os.environ["VECTOR_BACKEND"] = "local"
os.environ["EMBEDDING_MODE"] = "hash"
os.environ["RERANKER"] = "lexical"
os.environ["ANSWER_MODE"] = "lookup"
os.environ["OPENAI_API_KEY"] = ""

from backend.app.main import app
from backend.app.workflows.ingestion import POOL, CHECKPOINT


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as session:
        yield session
    POOL.shutdown(wait=True)
    CHECKPOINT.conn.close()
