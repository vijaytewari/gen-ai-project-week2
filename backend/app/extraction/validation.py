from decimal import Decimal, InvalidOperation


def review_issues(claim):
    return [{"field_id": f["id"], "group": f["group"],
             "message": f.get("ocr_warning", "Verify OCR against the source")}
            for f in claim["fields"] if f.get("requires_review") and not f.get("reviewed")
            and f["source"] == "ocr"]


def professional_issues(claim):
    issues = review_issues(claim)
    for field in claim["fields"]:
        if not field["value"] or not (field["id"] in ("1500.28", "1500.29")
                                      or field["id"].endswith(".charges")):
            continue
        try:
            value = Decimal(field["value"].replace(",", ""))
            if not value.is_finite() or value < 0:
                raise InvalidOperation
            if "." not in field["value"] and field["source"] == "ocr" and not field["reviewed"]:
                raise ValueError("OCR did not read a decimal separator; verify dollars and cents")
        except (ValueError, InvalidOperation) as exc:
            issues.append({"field_id": field["id"], "group": field["group"],
                           "message": str(exc) if isinstance(exc, ValueError) else "Check the amount format"})
    return issues
