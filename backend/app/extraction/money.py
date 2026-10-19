"""Normalize monetary OCR fields without changing their source evidence."""
import re
from decimal import Decimal


def is_money(field):
    key = field["id"]
    if key.startswith("1500."):
        return key in ("1500.28", "1500.29") or key.endswith(".charges")
    return field["locator"] in (47, 48, 54, 55) or (
        field["locator"] in (39, 40, 41) and key.endswith(".amount"))


def normalize_money(fields):
    changed = []
    for field in fields:
        if not is_money(field) or field.get("source") != "ocr":
            continue
        if not field["value"] or field.get("money_normalization"):
            continue
        raw = field["value"]
        digits = re.sub(r"[$,\s]", "", raw)
        if not re.fullmatch(r"-?\d+(?:\.\d{1,2})?", digits):
            continue
        implied = "." not in digits
        amount = Decimal(digits) / 100 if implied else Decimal(digits)
        field.update(value=f"{amount:.2f}", money_normalization="implied_cents" if implied
                     else "explicit_decimal", requires_review=True, reviewed=False)
        field["ocr_warning"] = ("Last two digits interpreted as cents. Verify against source."
                                if implied else "Verify dollars and cents against source.")
        changed.append(field["id"])
    return changed
