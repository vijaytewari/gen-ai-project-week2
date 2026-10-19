import cv2
import fitz
import numpy as np
from .engine import recognize, without_red
from .detection import detect
from .geometry import deskew, rotate


def read_page(page):
    scale = min(3.5, 2600 / max(page.rect.width, page.rect.height))
    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), colorspace=fitz.csRGB, alpha=False)
    original = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.height, pixmap.width, 3)
    original = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)
    prepared, skew_matrix, angle = deskew(original)
    best = None
    for orientation in (0, 90, 180, 270):
        image, orientation_matrix = rotate(prepared, orientation) if orientation else (prepared, np.eye(3))
        tokens = recognize(image)
        form, strength = detect(tokens)
        upright = image.shape[0] > image.shape[1]
        heading = next((t for t in tokens if "HEALTH" in t["text"].upper()
                        or "TYPE OF BILL" in t["text"].upper()), None)
        if heading and np.asarray(heading["polygon"])[:, 1].mean() > image.shape[0] / 2:
            upright = False
        score = strength * 100 + int(upright) * 1000
        if best is None or score > best[0]:
            best = (score, image, tokens, form, orientation_matrix @ skew_matrix, orientation)
        if upright and strength:
            break
        if orientation == 0 and not tokens:
            break
    _, image, tokens, form, matrix, orientation = best
    clean = without_red(image)
    changed = np.mean(clean != image)
    values = recognize(clean) if changed > .005 else tokens
    return {"tokens": tokens, "values": values, "form": form, "size": image.shape[:2][::-1],
            "inverse": np.linalg.inv(matrix), "original_size": (pixmap.width, pixmap.height),
            "rotation": page.rotation, "orientation": orientation, "deskew": angle,
            "page": page.number, "red_removed": bool(changed > .005), "clean_image": clean,
            "image": image}


def read_document(path):
    with fitz.open(path) as document:
        return [read_page(page) for page in document]
