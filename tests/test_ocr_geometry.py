import numpy as np
from backend.app.extraction.detection import detect
from backend.app.extraction.geometry import rotate, evidence
from backend.app.extraction.workflow import ensure_extracted
from backend.app.claims import create
from backend.app import database as db
import fitz


def test_rotation_transform_round_trips_evidence():
    image = np.ones((200, 100, 3), dtype=np.uint8) * 255
    _, matrix = rotate(image, 90)
    source = np.array([[10, 20, 1], [30, 20, 1], [30, 40, 1], [10, 40, 1]])
    polygon = (source @ matrix.T)[:, :2]
    result = evidence([{"polygon": polygon}], np.linalg.inv(matrix), (100, 200), 0, 0)
    assert np.allclose(result["box"], [.1, .1, .2, .1])
    assert detect([{"text": "UB-04 TYPE OF BILL STATEMENT COVERS"}])[0] == "CMS-1450"
    assert detect([{"text": "HEALTH INSURANCE CLAIM FORM NUCC FORM 1500"}])[0] == "CMS-1500"


def test_ocr_failure_is_visible_and_does_not_fabricate_values(client, tmp_path, monkeypatch):
    path = tmp_path / "scan.pdf"
    with fitz.open() as document:
        document.new_page()
        document.save(path)
    claim = create(path)
    claim["extraction"]["status"] = "pending"
    claim["revision"] = 2
    db.commit(claim, 1, {"action": "request_analysis"})
    def fail(_):
        raise ValueError("OCR engine unavailable")
    monkeypatch.setattr("backend.app.extraction.workflow.extract_document", fail)
    state = ensure_extracted({"claim_id": claim["id"], "revision": 2})
    result = db.load(claim["id"])
    assert state["revision"] == 3 and result["extraction"]["status"] == "failed"
    assert "unavailable" in result["extraction"]["error"]
    assert all(not f["value"] for f in result["fields"])
