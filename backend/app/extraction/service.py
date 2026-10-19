import time
from .pages import read_document
from .field_mapping import map_fields, form_groups
from ..fixtures import fields


def extract_document(path):
    started = time.perf_counter()
    pages = read_document(path)
    forms = [p["form"] for p in pages if p["form"] != "unknown"]
    form = max(set(forms), key=forms.count) if forms else "unknown"
    warnings = ["OCR values require human verification; handwriting recognition is not guaranteed."]
    if len(set(forms)) > 1:
        warnings.append("Mixed form types detected; mismatched pages were not mapped.")
    if form == "unknown":
        result, count, alignments = fields(empty=True), 0, []
        warnings.append("Form type was not recognized. Raw OCR text is available; use manual entry.")
    else:
        result, count, alignments = map_fields(pages, form)
    if form == "CMS-1500":
        warnings.append("CMS-1500 professional claim detected; CMS-1450 locator meanings were not used.")
    if "standard-page assumption" in alignments:
        warnings.append("Not enough readable labels for registration; standard-page mapping needs review.")
    if not count:
        warnings.append("No field values were mapped confidently. Inspect OCR text or enter values manually.")
    metadata = {"status": "complete", "engine": "RapidOCR ONNX 1.4.4", "mapped_fields": count,
                "form_type": form, "warnings": warnings, "alignments": alignments,
                "elapsed_ms": round((time.perf_counter() - started) * 1000),
                "pages": [{"page": p["page"], "orientation": p["orientation"],
                    "deskew_degrees": round(p["deskew"], 2), "red_removed": p["red_removed"],
                    "text": "\n".join(t["text"] for t in p["tokens"])} for p in pages]}
    return {"fields": result, "form_type": form, "groups": form_groups(form), "extraction": metadata}
