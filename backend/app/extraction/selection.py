import re
import numpy as np

LABELS = {"CITY", "STATE", "ZIPCODE", "DATE", "SIGNED", "NPI", "FROM", "THROUGH",
          "MMDDYY", "YES", "NO", "SEX", "CODE", "AMOUNT", "A", "B", "C", "D"}


def rectangle(token):
    points = np.asarray(token["polygon"])
    return (*points.min(axis=0), *points.max(axis=0))


def overlap(left, right):
    a, b, c, d = rectangle(left)
    e, f, g, h = rectangle(right)
    area = max(0, min(c, g) - max(a, e)) * max(0, min(d, h) - max(b, f))
    return area / max(1, min((c-a)*(d-b), (g-e)*(h-f)))


def select(page, box, allow_single=False):
    width, height = page["size"]
    left, top, right, bottom = np.array(box) * [width, height, width, height]
    chosen = []
    for token in page["tokens"] + page["values"]:
        x1, y1, x2, y2 = rectangle(token)
        x, y = (x1+x2)/2, (y1+y2)/2
        if not (left <= x < right and top <= y < bottom) or token["score"] < .6:
            continue
        if (min(x2, right) - max(x1, left)) / max(x2-x1, 1) < .65:
            continue
        compact = re.sub(r"[^A-Z0-9]", "", token["text"].upper())
        if len(compact) < (1 if allow_single else 2) or compact in LABELS or re.match(r"^FL\s*\d", token["text"], re.I):
            continue
        if not any(overlap(token, other) > .5 for other in chosen):
            chosen.append(token)
    return sorted(chosen, key=lambda t: (round(rectangle(t)[1] / 15), rectangle(t)[0]))
