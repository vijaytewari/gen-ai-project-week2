import re


def separate_totals(fields):
    """Revenue code 0001 / TOTAL is a summary, not another charge to add."""
    by_id = {field["id"]: field for field in fields}
    summaries = [f for f in fields if f["locator"] == 43
                 and re.fullmatch(r"TOTALS?", f["value"].strip(), re.I)]
    for description in summaries:
        row = description["row"]
        code = by_id.get(f"42.{row}", {}).get("value", "").strip()
        charge = by_id.get(f"47.{row}")
        if code not in ("001", "0001") or not charge or not charge["value"]:
            continue
        total = by_id["47.total"]
        for key in ("value", "original", "status", "evidence", "confidence", "source",
                    "requires_review", "ocr_warning"):
            total[key] = charge.get(key)
        for locator in range(42, 49):
            field = by_id.get(f"{locator}.{row}")
            if field:
                field.update(value="", status="not_applicable", requires_review=False,
                             ocr_warning="Summary row is shown in total charges")
