from copy import deepcopy
from .fixture_values import values
from .registry import GROUPS, label

VARIANTS = ["Clean print", "Handwriting-style", "Rotated scan", "Faint scan",
            "Missing boundaries", "Multipage services"]
SUBFIELDS = {3: ["a", "b"], 6: ["from", "through"], 31: ["code", "date"],
             39: ["code", "amount"], 67: ["principal", "other1"], 74: ["code", "date"]}


def field_keys(loc):
    if 42 <= loc <= 48:
        return [f"{loc}.{row}" for row in (1, 2)] + (["47.total"] if loc == 47 else [])
    if loc in list(range(50, 56)) + list(range(58, 66)):
        return [f"{loc}.{row}" for row in "ABC"]
    return [f"{loc}.{sub}" for sub in SUBFIELDS[loc]] if loc in SUBFIELDS else [str(loc)]


def fields(case=0, empty=False):
    source = {} if empty else values(case)
    result = []
    for group, _, locators in GROUPS:
        for loc in locators:
            for key in field_keys(loc):
                value = source.get(key, "")
                suffix = key.split(".", 1)[1] if "." in key else ""
                title = label(loc)
                if suffix in "ABC" and suffix and 50 <= loc <= 65:
                    suffix = {"A": "Primary", "B": "Secondary", "C": "Tertiary"}[suffix]
                if loc == 67:
                    title = "Principal diagnosis" if suffix == "principal" else "Other diagnosis"
                result.append({"id": key, "locator": loc, "group": group,
                    "label": title + (f" · {suffix}" if suffix else ""),
                    "row": suffix, "value": value, "original": value,
                    "status": "present" if value else "blank", "evidence": None,
                    "confidence": None if empty else (0.52 if case % 6 == 1 else 0.98),
                    "source": "manual" if empty else "curated", "reviewed": False})
    if not empty and case % 6 == 1:
        target = next(f for f in result if f["id"] == "60.A")
        target.update(value="", original="", status="unreadable", confidence=0.32)
    return result


def samples():
    return [{"id": i, "name": f"DEMO-{i + 1:04d}", "variant": VARIANTS[i % 6],
             "patient": values(i)["8"]} for i in range(12)]


def clone_fields(items):
    return deepcopy(items)
