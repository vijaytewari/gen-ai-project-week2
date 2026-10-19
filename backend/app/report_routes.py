import json
import threading
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from .config import REPORTS
from .workflows.ingestion import POOL

router = APIRouter(prefix="/api/reports")
LOCK = threading.Lock()
STATE = {"running": False, "error": ""}


@router.get("")
def list_reports():
    summaries = []
    for path in sorted(REPORTS.glob("*/summary.json"), reverse=True):
        summaries.append(json.loads(path.read_text(encoding="utf-8")))
    return {"reports": summaries[:10], **STATE}


def execute():
    from evaluation.run import run
    try:
        run()
    except Exception as exc:
        STATE["error"] = str(exc)[:400]
    finally:
        STATE["running"] = False


@router.post("/run")
def benchmark():
    with LOCK:
        if STATE["running"]:
            raise HTTPException(409, "A benchmark is already running")
        STATE.update(running=True, error="")
        POOL.submit(execute)
    return {"status": "queued"}


@router.get("/{run_id}/{name}")
def report_file(run_id: str, name: str):
    if not run_id.isdigit() and not (run_id.replace("T", "").isdigit()):
        raise HTTPException(404, "Run not found")
    if name not in ("CHUNKING_COMPARISON.md", "RERANKING_IMPACT.md", "manifest.json"):
        raise HTTPException(404, "Report not found")
    path = REPORTS / run_id / name
    if not path.exists():
        raise HTTPException(404, "Report not found")
    return FileResponse(path)
