from fastapi import APIRouter
from .library_store import records, saved_snapshot
from .registry import groups

router = APIRouter(prefix="/api")


@router.get("/library")
def library():
    return {"records": records(), "groups": groups()}


@router.get("/library/{claim_id}")
def saved_claim(claim_id: str):
    return saved_snapshot(claim_id)
