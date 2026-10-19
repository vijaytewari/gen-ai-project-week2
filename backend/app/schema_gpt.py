"""Generate field schema definitions from a value-free form catalog."""
import json
import httpx
from jsonschema import validate
from .config import setting


def generate(fields, form):
    key = setting("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not configured; using the local form schema.")
    catalog = [{"id": f["id"], "label": f["label"]} for f in fields]
    item = {"type": "object", "additionalProperties": False,
            "properties": {"id": {"type": "string", "enum": [f["id"] for f in fields]},
                           "kind": {"type": "string", "enum": ["text", "code", "date", "amount", "number"]},
                           "description": {"type": "string"}},
            "required": ["id", "kind", "description"]}
    schema = {"type": "object", "additionalProperties": False,
              "properties": {"definitions": {"type": "array", "items": item}},
              "required": ["definitions"]}
    response = httpx.post("https://api.openai.com/v1/responses", timeout=90,
        headers={"Authorization": f"Bearer {key}"}, json={
            "model": setting("OPENAI_SCHEMA_MODEL", "gpt-4.1-mini"), "store": False,
            "instructions": "Create a schema definition for EVERY supplied form field ID exactly once. "
                "Never invent IDs or patient values. Codes and identifiers remain strings. "
                "Amounts are decimal strings with two cent digits. Dates use ISO YYYY-MM-DD. "
                "Describe field meaning, not payer rules or coverage decisions.",
            "input": json.dumps({"form_type": form, "catalog": catalog}),
            "max_output_tokens": 16000,
            "text": {"format": {"type": "json_schema", "name": "form_definitions",
                                "strict": True, "schema": schema}}})
    response.raise_for_status()
    body = response.json()
    if body.get("status") != "completed":
        raise ValueError("GPT schema generation did not complete; using the local schema.")
    output = "".join(part.get("text", "") for message in body.get("output", [])
                     for part in message.get("content", []) if part.get("type") == "output_text")
    result = json.loads(output)
    validate(result, schema)
    definitions = result["definitions"]
    ids = [d["id"] for d in definitions]
    if len(ids) != len(set(ids)) or set(ids) != {f["id"] for f in fields}:
        raise ValueError("GPT schema omitted or duplicated fields; using the local schema.")
    return definitions
