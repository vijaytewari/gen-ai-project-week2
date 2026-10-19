import fitz


def test_registry_and_sample(client):
    library = client.get("/api/samples").json()
    locators = [loc for group in library["groups"] for loc in group["locators"]]
    assert sorted(locators) == list(range(1, 82))
    assert len(library["samples"]) == 12
    claim = client.post("/api/samples/0").json()
    assert len(claim["pages"]) <= 9
    assert claim["mode"] == "curated"
    assert "file" not in claim
    source = client.get(f"/api/claims/{claim['id']}/original")
    with fitz.open(stream=source.content, filetype="pdf") as doc:
        for field in claim["fields"]:
            evidence = field["evidence"]
            x, y, w, h = evidence["box"]
            assert 0 <= x < 1 and 0 <= y < 1 and x + w <= 1 and y + h <= 1
            assert f"FL {field['id']} " in doc[evidence["page"]].get_text()
            if field["value"]:
                assert field["value"] in doc[evidence["page"]].get_text()


def test_edits_conflicts_and_audit(client):
    claim = client.post("/api/samples/0").json()
    endpoint = f"/api/claims/{claim['id']}"
    payload = {"revision": 1, "changes": [{"field_id": "8", "value": "Corrected Demo"}]}
    saved = client.put(endpoint + "/fields", json=payload)
    assert saved.status_code == 200
    assert saved.json()["revision"] == 2
    field = next(f for f in saved.json()["fields"] if f["id"] == "8")
    assert field["original"] == "Jordan Reed" and field["value"] == "Corrected Demo"
    assert client.put(endpoint + "/fields", json=payload).status_code == 409
    export = client.get(endpoint + "/export").json()
    assert len(export["audit"]) == 1
    assert next(f for f in client.get(endpoint).json()["fields"] if f["id"] == "8")["value"] == "Corrected Demo"


def test_unmatched_upload_starts_ocr_without_dummy_values(client):
    document = fitz.open()
    document.new_page().insert_text((40, 40), "An arbitrary synthetic upload")
    response = client.post("/api/documents", files={"file": ("upload.pdf", document.tobytes(), "application/pdf")})
    assert response.status_code == 200
    claim = response.json()
    assert claim["mode"] == "uploaded" and claim["sample"] is None
    assert claim["extraction"]["status"] == "not_started"
    assert all(not f["value"] and f["evidence"] is None for f in claim["fields"])
    assert client.post("/api/documents", files={"file": ("bad.pdf", b"not a pdf")}).status_code == 415
    assert client.post("/api/documents", files={"file": ("bad.pdf", b"%PDF-broken")}).status_code == 422


def test_validation_and_acknowledgment(client):
    claim = client.post("/api/samples/0").json()
    base = f"/api/claims/{claim['id']}"
    changed = client.put(base + "/fields", json={"revision": 1, "changes": [
        {"field_id": "47.total", "value": "1.00"}]}).json()
    assert any("sum" in issue["message"] for issue in changed["issues"])
    assert client.post(base + "/review", json={"revision": 2, "group": "services"}).status_code == 422
    result = client.post(base + "/review", json={"revision": 2, "group": "services", "reason": "Demo discrepancy acknowledged"})
    assert result.status_code == 200 and "services" in result.json()["reviewed"]
