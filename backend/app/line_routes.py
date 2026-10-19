from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from . import database as db
from .claims import public
from .registry import label
from .workflows.ingestion import submit

router = APIRouter(prefix="/api/claims")


class AddLine(BaseModel):
    revision: int = Field(ge=1)


@router.post("/{claim_id}/service-lines")
def add_line(claim_id: str, request: AddLine):
    claim = db.load(claim_id)
    from .extraction.workflow import require_idle
    require_idle(claim)
    if claim.get("form_type") == "CMS-1500":
        raise HTTPException(422, "Edit the six detected professional service rows directly")
    if claim["revision"] != request.revision:
        raise HTTPException(409, "Reload before adding a service line")
    rows = [int(f["row"]) for f in claim["fields"]
            if f["group"] == "services" and f["row"].isdigit()]
    row = max(rows, default=0) + 1
    if row > 450:
        raise HTTPException(422, "Maximum 450 service lines")
    for loc in range(42, 49):
        claim["fields"].append({"id": f"{loc}.{row}", "locator": loc, "row": str(row),
            "group": "services", "label": f"{label(loc)} · {row}", "value": "",
            "original": "", "status": "blank", "evidence": None, "confidence": None,
            "source": "reviewer", "reviewed": False})
    claim["reviewed"] = [group for group in claim["reviewed"] if group != "services"]
    claim["acknowledgments"].pop("services", None)
    claim.update(revision=request.revision + 1, index_revision=None, saved_json=False)
    db.commit(claim, request.revision, {"actor": "Demo reviewer", "added_service_row": row})
    submit(claim_id)
    return public(claim)
