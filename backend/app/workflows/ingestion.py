import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command
from .. import database as db
from ..config import DATA
from ..rag.store import index_claim
from .source_checks import verify
from ..extraction.workflow import ensure_extracted

POOL = ThreadPoolExecutor(max_workers=1)
LOCK = threading.Lock()
CHECKPOINT = SqliteSaver(sqlite3.connect(DATA / "workflow.sqlite", check_same_thread=False))


class State(TypedDict, total=False):
    claim_id: str
    revision: int
    counts: dict
    issues: int


def review(state):
    interrupt({"claim_id": state["claim_id"], "revision": state["revision"],
               "action": "Review fields, then index this revision"})
    return {}


def build_index(state):
    claim = db.load(state["claim_id"])
    if claim["revision"] != state["revision"]:
        raise ValueError("Revision changed before indexing; retry current revision")
    db.job(claim["id"], "indexing")
    counts = index_claim(claim)
    with db.connection() as connection:
        row = connection.execute("SELECT revision FROM claims WHERE id=?", (claim["id"],)).fetchone()
        if row[0] != claim["revision"]:
            raise ValueError("Claim changed while indexing; retry current revision")
    db.job(claim["id"], f"ready:{claim['revision']}")
    return {"counts": counts}


builder = StateGraph(State)
builder.add_node("verify_source", verify)
builder.add_node("extract", ensure_extracted)
builder.add_node("review", review)
builder.add_node("index", build_index)
builder.add_edge(START, "verify_source")
builder.add_edge("verify_source", "extract")
builder.add_edge("extract", "review")
builder.add_edge("review", "index")
builder.add_edge("index", END)
GRAPH = builder.compile(checkpointer=CHECKPOINT)


def run(claim_id, approve=False):
    with LOCK:
        claim = db.load(claim_id)
        config = {"configurable": {"thread_id": f"{claim_id}:{claim['revision']}"}}
        try:
            state = GRAPH.get_state(config)
            if not state.values:
                GRAPH.invoke({"claim_id": claim_id, "revision": claim["revision"]}, config)
            elif state.next and state.next != ("review",):
                GRAPH.invoke(None, config)
            if approve:
                state = GRAPH.get_state(config)
                if state.next:
                    GRAPH.invoke(Command(resume=True) if state.next == ("review",) else None, config)
                else:
                    build_index({"claim_id": claim_id, "revision": claim["revision"]})
            else:
                db.job(claim_id, "awaiting_review")
        except Exception as exc:
            db.job(claim_id, "failed", str(exc)[:400])


def submit(claim_id, approve=False):
    db.job(claim_id, "queued")
    POOL.submit(run, claim_id, approve)
