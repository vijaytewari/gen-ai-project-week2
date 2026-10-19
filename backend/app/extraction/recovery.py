import json
from .. import database as db


def resume_pending():
    from ..workflows.ingestion import submit
    with db.connection() as connection:
        claims = [json.loads(row[0]) for row in connection.execute("SELECT body FROM claims")]
    for claim in claims:
        if claim.get("extraction", {}).get("status") == "pending":
            submit(claim["id"])
