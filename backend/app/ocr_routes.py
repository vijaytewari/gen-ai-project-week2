from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from . import database as db
from .claims import public
from .extraction.workflow import require_idle
from .workflows.ingestion import submit

router = APIRouter(prefix="/api/claims")


class OCRRequest(BaseModel):
    revision: int = Field(ge=1)


@router.post("/{claim_id}/ocr")
@router.post("/{claim_id}/analyze")
def rerun(claim_id: str, request: OCRRequest):
    claim = db.load(claim_id)
    if claim["revision"] != request.revision:
        raise HTTPException(409, "Reload the current revision before running OCR")
    if claim["sample"] is not None:
        raise HTTPException(422, "Curated fixtures already have known values; upload an image to run OCR")
    require_idle(claim)
    claim.update(revision=request.revision + 1, index_revision=None, saved_json=False,
                 extraction={"status": "pending", "warnings": []})
    db.commit(claim, request.revision, {"actor": "Reviewer", "action": "request_analysis"})
    submit(claim_id)
    return public(claim)
