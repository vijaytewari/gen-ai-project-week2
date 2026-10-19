import hashlib
import uuid
import fitz
from fastapi import HTTPException
from . import database as db
from .fixtures import fields
from .source_pdf import create_sample
from .validation import validate
from .registry import groups


def create(path, items=None, sample=None, filename=None, origin="upload"):
    with fitz.open(path) as doc:
        pages = [{"width": p.rect.width, "height": p.rect.height,
                  "rotation": p.rotation} for p in doc]
    claim = {"id": uuid.uuid4().hex, "revision": 1, "filename": filename or path.name,
             "file": str(path), "origin": origin, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
             "sample": sample, "mode": "curated" if items else "uploaded", "saved_json": False,
             "form_type": "CMS-1450" if items else "unknown", "groups": groups(),
             "extraction": {"status": "curated" if items else "not_started", "warnings": []},
             "pages": pages, "fields": items or fields(empty=True), "reviewed": [],
             "acknowledgments": {}, "index_revision": None}
    db.insert(claim)
    return claim


def sample(case):
    if not 0 <= case < 12:
        raise HTTPException(404, "Sample not found")
    path, items = create_sample(case)
    return create(path, items, case, filename=f"DEMO-{case + 1:04d}.pdf", origin="demo")


def public(claim):
    return {**{k: v for k, v in claim.items() if k != "file"},
            "issues": validate(claim), "job": db.job_status(claim["id"])}


def save(claim_id, request):
    claim = db.load(claim_id)
    from .extraction.workflow import require_idle
    require_idle(claim)
    if claim["revision"] != request.revision:
        raise HTTPException(409, "Claim changed. Reload before saving.")
    lookup = {f["id"]: f for f in claim["fields"]}
    events = []
    for change in request.changes:
        if change.field_id not in lookup:
            raise HTTPException(422, "Unknown field")
        field = lookup[change.field_id]
        if change.status != "present" and change.value:
            raise HTTPException(422, "Non-present values must be empty")
        if change.status == "present" and not change.value.strip():
            raise HTTPException(422, "Present values must contain text")
        events.append({"field_id": field["id"], "old": field["value"], "new": change.value,
                       "old_status": field["status"], "new_status": change.status})
        field.update(value=change.value, status=change.status, source="reviewer", reviewed=False,
                     requires_review=False, ocr_warning="")
        claim["reviewed"] = [g for g in claim["reviewed"] if g != field["group"]]
        claim["acknowledgments"].pop(field["group"], None)
    claim.update(revision=request.revision + 1, index_revision=None, saved_json=True)
    from .form_schema import attach_data
    attach_data(claim)
    db.commit(claim, request.revision, {"actor": request.actor, "changes": events})
    from .library_store import publish
    publish(claim)
    return claim
