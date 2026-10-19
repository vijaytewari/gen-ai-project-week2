from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import database as db
from .config import ROOT, setting
from .routes import router


@asynccontextmanager
async def lifespan(app):
    db.initialize()
    from .extraction.money_migration import migrate_money
    migrate_money()
    from .extraction.recovery import resume_pending
    resume_pending()
    yield


app = FastAPI(title="Claims Processor", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=setting("CORS_ORIGINS",
    "http://localhost:5173").split(","), allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type"])
app.include_router(router)
from .library_routes import router as library_router
app.include_router(library_router)
from .line_routes import router as line_router
app.include_router(line_router)
from .ocr_routes import router as ocr_router
app.include_router(ocr_router)


@app.exception_handler(ValueError)
async def value_error(request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)[:400]})


@app.get("/api/health")
def health():
    return {"status": "ok", "backend": setting("VECTOR_BACKEND", "local"),
            "embedding": setting("EMBEDDING_MODE", "hash"),
            "reranker": setting("RERANKER", "lexical"), "mode": "synthetic-demo"}


from .report_routes import router as reports_router
app.include_router(reports_router)
dist = ROOT / "frontend" / "dist"
if dist.exists():
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")


@app.get("/")
def home():
    if dist.exists():
        return FileResponse(dist / "index.html")
    return {"message": "Run the Vite frontend on port 5173 or build frontend/dist"}
