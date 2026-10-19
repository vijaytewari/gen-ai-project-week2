"""Versioned JSON Schema and local validation of the complete form_data object."""
from jsonschema import Draft202012Validator, FormatChecker
from .extraction.money import is_money

PATTERNS = {"amount": r"^\d+\.\d{2}$", "number": r"^\d+(?:\.\d+)?$"}


def local_kind(field):
    if is_money(field):
        return "amount"
    if "date" in field["label"].lower() or field["id"] in ("6.from", "6.through"):
        return "date"
    return "text"


def build(fields, definitions=()):
    proposed = {d["id"]: d for d in definitions}
    properties = {}
    for field in fields:
        definition = proposed.get(field["id"], {})
        kind = "amount" if is_money(field) else definition.get("kind", local_kind(field))
        rule = {"type": "string"}
        if kind in PATTERNS:
            rule["pattern"] = PATTERNS[kind]
        if kind == "date":
            rule["format"] = "date"
        properties[field["id"]] = {"title": field["label"],
            "description": definition.get("description", field["label"]),
            "anyOf": [{"const": ""}, rule]}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
            "properties": properties, "required": list(properties), "additionalProperties": False}


def attach_data(claim):
    claim.setdefault("schema_generation", {"source": "local", "status": "not_requested",
                     "message": "Local schema. Press Analyzer to request GPT schema generation."})
    fields = claim["fields"]
    schema = claim.get("form_schema") or build(fields)
    if set(schema["properties"]) != {f["id"] for f in fields}:
        updated = build(fields)
        for key in updated["properties"]:
            if key in schema["properties"]:
                updated["properties"][key] = schema["properties"][key]
        schema = updated
    claim["form_schema"] = schema
    claim["form_data"] = {f["id"]: f["value"] for f in fields}
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [{"field_id": str(next(iter(error.path), "")), "message": "Value does not match the form schema"}
              for error in validator.iter_errors(claim["form_data"])]
    claim["schema_validation"] = {"valid": not errors, "errors": errors,
                                  "engine": "JSON Schema Draft 2020-12 (local)"}


def analyze_schema(claim):
    from .schema_gpt import generate
    from .config import setting
    definitions = []
    metadata = {"source": "local", "status": "fallback", "message": "Local form schema"}
    try:
        definitions = generate(claim["fields"], claim["form_type"])
        metadata = {"source": "gpt", "status": "complete",
                    "model": setting("OPENAI_SCHEMA_MODEL", "gpt-4.1-mini"),
                    "message": "GPT generated schema; values validated locally. Human review required."}
    except Exception as exc:
        metadata["message"] = str(exc) if isinstance(exc, ValueError) else "GPT schema request failed; using local schema."
    claim["form_schema"] = build(claim["fields"], definitions)
    claim["schema_generation"] = metadata
    attach_data(claim)
