import json
import sqlite3
from contextlib import contextmanager
from fastapi import HTTPException
from .config import DATA


@contextmanager
def connection():
    db = sqlite3.connect(DATA / "claims.sqlite", timeout=30)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def initialize():
    with connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS claims(id TEXT PRIMARY KEY, revision INTEGER, body TEXT);
        CREATE TABLE IF NOT EXISTS history(id TEXT, revision INTEGER, body TEXT,
          PRIMARY KEY(id, revision));
        CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, claim_id TEXT,
          timestamp TEXT DEFAULT CURRENT_TIMESTAMP, body TEXT);
        CREATE TABLE IF NOT EXISTS jobs(claim_id TEXT PRIMARY KEY, status TEXT, error TEXT);
        CREATE TABLE IF NOT EXISTS saved_json(id TEXT PRIMARY KEY, revision INTEGER, body TEXT);
        """)


def load(claim_id):
    with connection() as db:
        row = db.execute("SELECT body FROM claims WHERE id=?", (claim_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Claim not found")
    return json.loads(row[0])


def insert(claim):
    body = json.dumps(claim)
    with connection() as db:
        db.execute("INSERT INTO claims VALUES(?,?,?)", (claim["id"], claim["revision"], body))
        db.execute("INSERT INTO history VALUES(?,?,?)", (claim["id"], claim["revision"], body))



def commit(claim, expected, event):
    event = {**event, "revision": claim["revision"]}
    body = json.dumps(claim)
    with connection() as db:
        changed = db.execute("UPDATE claims SET revision=?, body=? WHERE id=? AND revision=?",
            (claim["revision"], body, claim["id"], expected)).rowcount
        if not changed:
            raise HTTPException(409, "Claim changed. Reload before saving.")
        db.execute("INSERT INTO history VALUES(?,?,?)", (claim["id"], claim["revision"], body))
        db.execute("INSERT INTO audit(claim_id,body) VALUES(?,?)",
                   (claim["id"], json.dumps(event)))


def job(claim_id, status, error=""):
    with connection() as db:
        db.execute("INSERT OR REPLACE INTO jobs VALUES(?,?,?)", (claim_id, status, error))


def job_status(claim_id):
    with connection() as db:
        row = db.execute("SELECT status,error FROM jobs WHERE claim_id=?", (claim_id,)).fetchone()
    return dict(row) if row else {"status": "pending", "error": ""}
