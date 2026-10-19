from fastapi import HTTPException
from . import database as db
from .registry import groups
from .validation import validate


def mark_reviewed(claim_id, request):
    claim = db.load(claim_id)
    from .extraction.workflow import require_idle
    require_idle(claim)
    if claim["revision"] != request.revision:
        raise HTTPException(409, "Claim changed. Reload before review.")
    if request.group not in {g["id"] for g in claim.get("groups", groups())}:
        raise HTTPException(422, "Unknown group")
    issues = [i for i in validate(claim) if i["group"] == request.group]
    if issues and not request.reason.strip():
        raise HTTPException(422, "Resolve issues or supply an acknowledgment reason")
    claim["reviewed"] = sorted(set(claim["reviewed"] + [request.group]))
    if request.reason:
        claim["acknowledgments"][request.group] = request.reason
    for field in claim["fields"]:
        if field["group"] == request.group:
            field["reviewed"] = True
    claim.update(revision=request.revision + 1, index_revision=None)
    db.commit(claim, request.revision, {"actor": "Reviewer", "review": request.group,
                                      "reason": request.reason})
    from .library_store import publish
    publish(claim)
    return claim
