import re
import fitz
import pytest
from backend.app.config import ROOT
from backend.app.extraction.service import extract_document
from backend.app.extraction.detection import detect


def test_structure_detection_requires_distinct_revenue_codes():
    headings = [{"text": "CREATION DATE"}, {"text": "TOTALS"}]
    assert detect(headings)[0] == "unknown"
    assert detect(headings + [{"text": "210"}] * 5)[0] == "unknown"
    codes = [{"text": code} for code in ("210", "250", "270", "300")]
    assert detect(headings + codes)[0] == "CMS-1450"


def test_photographed_institutional_form_maps_correct_fields(tmp_path):
    source = ROOT / "sample1450.JPG"
    if not source.exists():
        pytest.skip("User-provided institutional example is not present")
    path = tmp_path / "institutional.pdf"
    with fitz.open(source) as image:
        path.write_bytes(image.convert_to_pdf())
    result = extract_document(path)
    assert result["form_type"] == "CMS-1450"
    assert result["extraction"]["mapped_fields"] >= 45
    assert "grid-aligned fallback" in result["extraction"]["alignments"]
    fields = {field["id"]: field for field in result["fields"]}
    assert "COLLEGEHOSPITAL" in re.sub(r"\W", "", fields["1"]["value"])
    assert re.sub(r"\W", "", fields["8"]["value"]) == "TORREMARYJ"
    assert fields["4"]["value"] == "0111"
    assert fields["11"]["value"] == "F"
    assert fields["42.1"]["value"] == "210" and fields["46.1"]["value"] == "3"
    assert fields["42.8"]["value"] == "730"
    assert fields["47.total"]["value"] == "15171.50"
    assert fields["47.9"]["status"] == "not_applicable"
    assert fields["47.9"]["original"] == fields["47.total"]["original"]
    assert "cents" in fields["47.total"]["ocr_warning"]
    assert fields["8"]["evidence"]["box"][1] > .13
