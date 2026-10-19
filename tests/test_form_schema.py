import json
from jsonschema import Draft202012Validator
from backend.app.fixtures import fields
from backend.app.form_schema import analyze_schema, attach_data, build


def test_complete_schema_preserves_blanks_codes_and_amounts(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")
    claim = {"fields": fields(), "form_type": "CMS-1450"}
    analyze_schema(claim)
    assert claim["schema_generation"]["source"] == "local"
    assert "OPENAI_API_KEY" in claim["schema_generation"]["message"]
    assert set(claim["form_data"]) == set(claim["form_schema"]["required"])
    assert claim["form_data"]["47.total"] == "1450.00"
    Draft202012Validator.check_schema(claim["form_schema"])
    target = next(f for f in claim["fields"] if f["id"] == "47.total")
    target["value"] = "145000"
    attach_data(claim)
    assert not claim["schema_validation"]["valid"]
    assert any(e["field_id"] == "47.total" for e in claim["schema_validation"]["errors"])


def test_gpt_uses_only_catalog_and_its_schema_is_used(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    claim = {"fields": fields(), "form_type": "CMS-1450"}
    definitions = [{"id": f["id"], "kind": "text", "description": "GPT field description"}
                   for f in claim["fields"]]
    captured = {}
    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status": "completed", "output": [{"content": [
                {"type": "output_text", "text": json.dumps({"definitions": definitions})}]}]}
    def post(url, **kwargs):
        captured.update(kwargs["json"])
        return Response()
    monkeypatch.setattr("backend.app.schema_gpt.httpx.post", post)
    analyze_schema(claim)
    assert claim["schema_generation"]["source"] == "gpt"
    assert claim["form_schema"]["properties"]["8"]["description"] == "GPT field description"
    assert "Jordan Reed" not in json.dumps(captured)
    assert "value" not in json.loads(captured["input"])["catalog"][0]
    assert captured["store"] is False
    # Even a GPT text suggestion cannot remove the required money representation.
    assert "pattern" in claim["form_schema"]["properties"]["47.total"]["anyOf"][1]
    definitions.pop()
    analyze_schema(claim)
    assert claim["schema_generation"]["source"] == "local"
