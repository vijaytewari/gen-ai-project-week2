from fastapi import HTTPException
from .. import database as db
from .service import extract_document


def pending(claim):
    return claim.get("extraction", {}).get("status") == "pending"


def ensure_extracted(state):
    claim = db.load(state["claim_id"])
    if not pending(claim) or claim["sample"] is not None:
        return {}
    expected = claim["revision"]
    db.job(claim["id"], "ocr")
    try:
        result = extract_document(claim["file"])
        corrections = [f for f in claim["fields"] if f["source"] == "reviewer"]
        keys = {f["id"] for f in result["fields"]}
        if any(f["id"] not in keys for f in corrections):
            raise ValueError("Detected form changes existing field IDs. Upload a fresh copy to preserve corrections.")
        protected = {f["id"]: f for f in corrections}
        result["fields"] = [protected.get(f["id"], f) for f in result["fields"]]
        claim.update(result, mode="ocr", reviewed=[], acknowledgments={}, index_revision=None)
        from ..form_schema import analyze_schema
        analyze_schema(claim)
        claim["saved_json"] = False
        event = {"actor": "Local OCR", "form_type": claim["form_type"],
                 "mapped_fields": claim["extraction"]["mapped_fields"]}
    except Exception as exc:
        message = str(exc)[:250] if isinstance(exc, (ValueError, ImportError)) else type(exc).__name__
        claim["extraction"] = {"status": "failed", "error": message,
                                "warnings": ["OCR failed. Retry or enter fields manually."]}
        claim["mode"] = "manual"
        event = {"actor": "Local OCR", "status": "failed", "error": message}
    claim["revision"] = expected + 1
    db.commit(claim, expected, event)
    return {"revision": claim["revision"]}


def require_idle(claim):
    if pending(claim):
        raise HTTPException(409, "OCR is running. Wait for extraction before editing or indexing.")
