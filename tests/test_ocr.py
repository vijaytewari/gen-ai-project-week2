import copy
import time
from pathlib import Path
import fitz
import pytest
from backend.app.config import ROOT
from backend.app.extraction.service import extract_document


@pytest.fixture(scope="module")
def sample_ocr(tmp_path_factory):
    source = ROOT / "cms1450Form_Sample.JPG"
    if not source.exists():
        pytest.skip("User-provided professional sample is not present")
    target = tmp_path_factory.mktemp("ocr") / "sample.pdf"
    with fitz.open(source) as image:
        target.write_bytes(image.convert_to_pdf())
    return extract_document(target)


def wait_ocr(client, claim_id):
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        claim = client.get(f"/api/claims/{claim_id}").json()
        if claim["extraction"]["status"] != "pending":
            return claim
        time.sleep(.1)
    raise AssertionError("OCR did not finish")


def test_real_sample_detects_professional_schema_and_maps_values(sample_ocr):
    assert sample_ocr["form_type"] == "CMS-1500"
    assert sample_ocr["extraction"]["mapped_fields"] >= 20
    fields = {f["id"]: f for f in sample_ocr["fields"]}
    assert "Jane" in fields["1500.2"]["value"]
    assert fields["1500.26"]["value"]
    assert "8" not in fields
    for field in fields.values():
        if field["value"]:
            assert field["requires_review"] and field["source"] == "ocr"
            assert all(0 <= number <= 1 for number in field["evidence"]["box"])


def test_analyzer_and_retry_preserve_corrections(client, monkeypatch, sample_ocr):
    monkeypatch.setattr("backend.app.extraction.workflow.extract_document",
                        lambda _: copy.deepcopy(sample_ocr))
    image = (ROOT / "cms1450Form_Sample.JPG").read_bytes()
    response = client.post("/api/documents", files={"file": ("misnamed-cms1450.jpg", image)})
    assert response.status_code == 200
    uploaded = response.json()
    assert uploaded["extraction"]["status"] == "not_started"
    client.post(f"/api/claims/{uploaded['id']}/analyze", json={"revision": 1})
    claim = wait_ocr(client, uploaded["id"])
    assert claim["mode"] == "ocr" and claim["revision"] == 3
    base = f"/api/claims/{claim['id']}"
    saved = client.put(base + "/fields", json={"revision": 3, "changes": [
        {"field_id": "1500.2", "value": "Reviewer verified name"}]}).json()
    assert saved["revision"] == 4
    retry = client.post(base + "/ocr", json={"revision": 4})
    assert retry.status_code == 200
    result = wait_ocr(client, claim["id"])
    field = next(f for f in result["fields"] if f["id"] == "1500.2")
    assert field["value"] == "Reviewer verified name" and field["source"] == "reviewer"
    assert client.post(base + "/ocr", json={"revision": 1}).status_code == 409
