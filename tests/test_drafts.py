import fitz
from backend.app import database as db


def test_upload_and_preview_never_publish_but_explicit_save_does(client):
    with fitz.open() as source:
        source.new_page()
        payload = source.tobytes()
    claim = client.post("/api/documents", files={"file": ("draft.pdf", payload)}).json()
    base = f"/api/claims/{claim['id']}"
    assert claim["extraction"]["status"] == "not_started"
    assert db.job_status(claim["id"])["status"] == "pending"
    assert client.get(base + "/export").status_code == 200
    assert client.get(f"/api/library/{claim['id']}").status_code == 404
    records = client.get("/api/library").json()["records"]
    assert not any(r["id"] == claim["id"] for r in records)
    saved = client.put(base + "/fields", json={"revision": 1, "changes": []}).json()
    assert saved["saved_json"] and saved["revision"] == 2
    published = client.get(f"/api/library/{claim['id']}").json()
    assert published["schema_validation"]["valid"]
    assert len(published["form_data"]) == len(published["fields"])
    # Background analysis/review revisions do not change the explicitly saved JSON.
    draft = db.load(claim["id"])
    draft.update(revision=3, saved_json=False)
    db.commit(draft, 2, {"action": "draft_analysis"})
    assert client.get(f"/api/library/{claim['id']}").json() == published
    client.put(base + "/fields", json={"revision": 3, "changes": []})
    records = client.get("/api/library").json()["records"]
    assert len([r for r in records if r["id"] == claim["id"]]) == 1
    assert next(r for r in records if r["id"] == claim["id"])["revision"] == 4
