import hashlib
from pathlib import Path
from .. import database as db
from ..validation import validate


def verify(state):
    claim = db.load(state["claim_id"])
    if claim["revision"] != state["revision"]:
        raise ValueError("Claim changed before processing; reload and retry")
    digest = hashlib.sha256(Path(claim["file"]).read_bytes()).hexdigest()
    if digest != claim["sha256"]:
        raise ValueError("Original document checksum changed; source verification failed")
    return {"issues": len(validate(claim))}
