import os
import subprocess
import sys
from backend.app import database as db
from backend.app.claims import sample
from backend.app.config import ROOT
from backend.app.workflows.ingestion import run


def test_human_review_checkpoint_resumes_in_a_new_process(client):
    claim = sample(0)
    run(claim["id"])
    assert db.job_status(claim["id"])["status"] == "awaiting_review"
    command = ("from backend.app.workflows.ingestion import run; "
               f"run('{claim['id']}', approve=True)")
    child = subprocess.run([sys.executable, "-c", command], cwd=ROOT,
                           env=os.environ.copy(), capture_output=True, text=True, timeout=45)
    assert child.returncode == 0, child.stderr
    assert db.job_status(claim["id"])["status"] == "ready:1"
