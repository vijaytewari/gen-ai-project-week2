import re
import cv2
import numpy as np
from .grid_alignment import align_grid

ANCHORS = {
    "CMS-1500": [("HEALTHINSURANCECLAIMFORM", (.032, .079)),
                 ("PATIENTSNAME", (.034, .16)), ("FEDERALTAX", (.034, .839)),
                 ("TOTALCHARGE", (.605, .839)), ("INSUREDSIDNUMBER", (.602, .13))],
    "CMS-1450": [("TYPEOFBILL", (.896, .051)), ("STATEMENTCOVERS", (.711, .078)),
                 ("REVCD", (.044, .277)), ("TOTALCHARGES", (.705, .277)),
                 ("PAYERNAME", (.044, .609)), ("INSUREDSNAME", (.044, .665))],
}


def align(page, form):
    source, target = [], []
    width, height = page["size"]
    for pattern, nominal in ANCHORS.get(form, []):
        match = next((t for t in page["tokens"] if pattern in
                      re.sub(r"[^A-Z0-9]", "", t["text"].upper())), None)
        if match:
            source.append(nominal)
            target.append(np.asarray(match["polygon"])[0] / [width, height])
    if len(source) >= 3:
        matrix, inliers = cv2.estimateAffinePartial2D(np.float32(source), np.float32(target),
                                                   ransacReprojThreshold=.02)
        if matrix is not None and inliers.sum() >= 3:
            scale = np.linalg.norm(matrix[:, 0])
            if .75 < scale < 1.25 and np.max(np.abs(matrix[:, 2])) < .15:
                return matrix, "label-aligned"
    matrix = align_grid(page) if form == "CMS-1450" else None
    if matrix is not None:
        return matrix, "grid-aligned fallback"
    return np.array([[1., 0., 0.], [0., 1., 0.]]), "standard-page assumption"


def transform_box(box, matrix):
    x1, y1, x2, y2 = box
    points = np.array([[x1, y1, 1], [x2, y2, 1]]) @ matrix.T
    return (*points[0], *points[1])
