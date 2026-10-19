import json
from backend.app.config import DATA


def test_legacy_demo_records_are_hidden_but_explicit_uploads_remain_visible():
    from backend.app.library_store import visible
    legacy = {"sample": 0, "filename": "sample-0.pdf"}
    assert not visible(legacy)
    assert not visible({**legacy, "origin": "upload"})
    assert visible({**legacy, "origin": "upload", "saved_json": True})


def test_uploaded_claim_library_contains_complete_json_and_every_edit(client):
    demo = client.post("/api/samples/0").json()
    source = client.get(f"/api/claims/{demo['id']}/original").content
    claim = client.post("/api/documents", files={
        "file": ("synthetic-library.pdf", source, "application/pdf")}).json()
    base = f"/api/claims/{claim['id']}"
    assert not any(r["id"] == claim["id"] for r in client.get("/api/library").json()["records"])
    initial = client.get(base + "/export").json()
    assert {f["locator"] for f in initial["fields"]} == set(range(1, 82))
    assert any(f["value"] == "" for f in initial["fields"])
    for revision, value in [(1, "Synthetic first edit"), (2, "Synthetic second edit")]:
        response = client.put(base + "/fields", json={"revision": revision,
            "changes": [{"field_id": "8", "value": value}]})
        assert response.status_code == 200
    records = client.get("/api/library").json()["records"]
    assert not any(record["id"] == demo["id"] for record in records)
    record = next(record for record in records if record["id"] == claim["id"])
    assert record["revision"] == 3 and record["edit_count"] == 2
    exported = client.get(base + "/export").json()
    assert len(exported["fields"]) == len(initial["fields"])
    assert [r["revision"] for r in exported["revisions"]] == [1, 2, 3]
    assert len(exported["audit"]) == 2
    changes = [event["event"]["changes"][0] for event in exported["audit"]]
    assert changes[0]["old"] == "Jordan Reed"
    assert changes[1]["old"] == "Synthetic first edit"
    assert changes[1]["new"] == "Synthetic second edit"
    assert "file" not in exported and all("file" not in r for r in exported["revisions"])
    stored = DATA / "json" / f"{claim['id']}.json"
    assert json.loads(stored.read_text(encoding="utf-8")) == exported
    conflict = client.put(base + "/fields", json={"revision": 1,
        "changes": [{"field_id": "8", "value": "Stale edit"}]})
    assert conflict.status_code == 409
    assert len(client.get(base + "/export").json()["audit"]) == 2
    from backend.app.library_store import snapshot
    historical = snapshot(initial)
    assert historical["revision"] == 1
    assert len(historical["revisions"]) == 1
    assert historical["audit"] == []
