import re
from .geometry import evidence
from .registration import align, transform_box
from .selection import select
from .crops import read_crop
from .totals import separate_totals
from .money import normalize_money
from . import schema1500, layout1450
from ..fixtures import fields
from ..registry import groups, label


def empty_field(key, title, group):
    number = re.match(r"\d+", key).group()
    row = key.split(".")[1] if key.startswith("24.") else ""
    return {"id": f"1500.{key}", "locator": int(number), "label": title, "group": group,
            "row": row, "value": "", "original": "", "status": "blank", "evidence": None,
            "confidence": None, "source": "ocr", "reviewed": False}


def targets(form, pages):
    if form == "CMS-1500":
        definitions = schema1500.definitions()
        return [empty_field(k, title, group) for k, title, group, _ in definitions]
    result = fields(empty=True)
    synthetic = any("CLAIMLENS" in t["text"].upper() for p in pages for t in p["tokens"])
    if not synthetic:
        for row in range(3, 22 * len(pages) + 1):
            for locator in range(42, 49):
                item = next(f for f in result if f["id"] == f"{locator}.1").copy()
                item.update(id=f"{locator}.{row}", row=str(row), label=f"{label(locator)} · {row}")
                result.append(item)
    return result


def map_fields(pages, form):
    result = targets(form, pages)
    windows1500 = {f"1500.{key}": box for key, _, _, box in schema1500.definitions()}
    mapped, alignments = 0, []
    for page in pages:
        if page["form"] != form:
            continue
        matrix, alignment = align(page, form)
        alignments.append(alignment)
        synthetic = any("CLAIMLENS" in t["text"].upper() for t in page["tokens"])
        for field in result:
            if field["value"]:
                continue
            if form == "CMS-1450" and not synthetic and field["group"] == "services" and field["row"].isdigit():
                if (int(field["row"]) - 1) // 22 != page["page"]:
                    continue
            box = windows1500[field["id"]] if form == "CMS-1500" else layout1450.window(field, synthetic)
            if box is None:
                continue
            box = transform_box(box, matrix) if not synthetic else box
            allow_single = field["locator"] in (11, 13, 14, 15, 16, 17, 46, 52, 53, 66)
            hits = select(page, box, allow_single)
            if not hits:
                hits = read_crop(page, box)
            if not hits:
                continue
            value = " ".join(t["text"] for t in hits)
            field.update(value=value, original=value, status="present", source="ocr",
                         confidence=round(sum(t["score"] for t in hits) / len(hits), 3),
                         evidence=evidence(hits, page["inverse"], page["original_size"],
                                           page["page"], page["rotation"]),
                         requires_review=True, ocr_warning="Verify OCR text and field placement against the source.")
            if field["locator"] in (47, 48, 54, 55) and "." not in value:
                field["ocr_warning"] = "Decimal separator not recognized; verify dollars and cents."
            mapped += 1
    if form == "CMS-1450":
        separate_totals(result)
    normalize_money(result)
    return result, sum(bool(f["value"]) for f in result), sorted(set(alignments))


def form_groups(form):
    return schema1500.groups() if form == "CMS-1500" else groups()
