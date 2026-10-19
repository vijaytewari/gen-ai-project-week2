from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import Response, FileResponse
from . import database as db
from .claims import sample, public, save
from .documents import upload, page_image
from .fixtures import samples
from .registry import groups
from .models import SaveRequest, ReviewRequest, Question
from .review import mark_reviewed
from .workflows.ingestion import submit
from .workflows.question import ask

router = APIRouter(prefix="/api")


@router.get("/samples")
def list_samples():
    return {"samples": samples(), "groups": groups()}


@router.post("/samples/{case}")
def open_sample(case: int):
    claim = sample(case)
    submit(claim["id"])
    return public(claim)


@router.post("/documents")
async def upload_document(file: UploadFile):
    claim = await upload(file)
    return public(claim)


@router.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    return public(db.load(claim_id))


@router.get("/claims/{claim_id}/pages/{page}")
def image(claim_id: str, page: int):
    return Response(page_image(db.load(claim_id), page), media_type="image/png")


@router.get("/claims/{claim_id}/original")
def original(claim_id: str):
    return FileResponse(db.load(claim_id)["file"], media_type="application/pdf")


@router.put("/claims/{claim_id}/fields")
def update_fields(claim_id: str, request: SaveRequest):
    claim = save(claim_id, request)
    submit(claim_id)
    return public(claim)


@router.post("/claims/{claim_id}/review")
def review(claim_id: str, request: ReviewRequest):
    claim = mark_reviewed(claim_id, request)
    submit(claim_id)
    return public(claim)


@router.post("/claims/{claim_id}/index")
def index(claim_id: str):
    from .extraction.workflow import require_idle
    require_idle(db.load(claim_id))
    submit(claim_id, approve=True)
    return {"status": "queued"}


@router.post("/claims/{claim_id}/questions")
def question(claim_id: str, request: Question):
    claim = db.load(claim_id)
    if claim["revision"] != request.revision:
        raise HTTPException(409, "Reload the current claim revision")
    if db.job_status(claim_id)["status"] != f"ready:{claim['revision']}":
        raise HTTPException(409, "Index the current revision before asking questions")
    return ask(claim, request)


@router.get("/claims/{claim_id}/export")
def export(claim_id: str):
    from .library_store import snapshot
    return snapshot(db.load(claim_id))
