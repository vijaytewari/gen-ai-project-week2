import hashlib
import fitz
from .config import FILES
from .fixtures import fields
from .form_layout import base_box, field_box


def create_sample(case):
    """Render only our own synthetic layout and fictional values."""
    items = fields(case)
    doc = fitz.open()
    pages = 2 if case % 6 == 5 else 1
    for page_number in range(pages):
        page = doc.new_page(width=850, height=1100)
        page.insert_text((20, 24), "CLAIMLENS / CMS-1450 SYNTHETIC REVIEW COPY", fontsize=12)
        page.insert_text((20, 38), "Not an official UB-04. Not for billing. All data is fictional.",
                         fontsize=7, color=(0.55, 0.2, 0.2))
        for loc in range(1, 82):
            x, y, width, height = base_box(loc)
            if case % 6 != 4:
                page.draw_rect(fitz.Rect(x, y, x + width, y + height),
                               color=(0.7, 0.35, 0.35), width=0.45)
        for field in items:
            siblings = [f for f in items if f["locator"] == field["locator"]]
            x, y, width, height = field_box(field, siblings)
            continuation = pages == 2 and field["group"] == "services" and field["row"] != "1"
            evidence_page = 1 if continuation else 0
            field["evidence"] = {"page": evidence_page, "box": [x / 850, y / 1100,
                                                                  width / 850, height / 1100]}
            if page_number != evidence_page:
                continue
            color = (0.57, 0.6, 0.61) if case % 6 == 3 else (0.12, 0.22, 0.25)
            page.insert_text((x + 2, y + 5), f"FL {field['id']}  {field['label']}"[:int(width / 2.7)],
                             fontsize=4.7, color=(0.6, 0.3, 0.3))
            text = field["value"] or ("[unreadable]" if field["status"] == "unreadable" else "")
            page.insert_text((x + 3, y + min(height - 2, 17)), text,
                             fontsize=min(6, height / 3.5), color=color,
                             fontname="heit" if case % 6 == 1 else "helv")
        page.insert_text((20, 1060), f"DEMO-{case + 1:04d} | Page {page_number + 1} / {pages}", fontsize=8)
        if case % 6 == 2:
            page.set_rotation(90)
    payload = doc.tobytes(no_new_id=True)
    digest = hashlib.sha256(payload).hexdigest()[:16]
    path = FILES / f"sample-{case}-{digest}.pdf"
    path.write_bytes(payload)
    doc.close()
    return path, items
