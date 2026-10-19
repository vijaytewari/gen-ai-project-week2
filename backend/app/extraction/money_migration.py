"""Version existing OCR amounts once; leave reviewer corrections untouched."""
import json
from .. import database as db
from .money import normalize_money


def migrate_money():
    with db.connection() as connection:
        claims = connection.execute("SELECT body FROM claims").fetchall()
    for row in claims:
        claim = json.loads(row[0])
        changed = normalize_money(claim["fields"])
        if not changed:
            continue
        groups = {f["group"] for f in claim["fields"] if f["id"] in changed}
        claim["reviewed"] = [g for g in claim["reviewed"] if g not in groups]
        for group in groups:
            claim.get("acknowledgments", {}).pop(group, None)
        previous = claim["revision"]
        claim.update(revision=previous + 1, index_revision=None)
        db.commit(claim, previous, {"action": "normalize_ocr_money", "fields": changed})
        db.job(claim["id"], "awaiting_review")
