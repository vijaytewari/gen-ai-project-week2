import re
import cv2
import numpy as np
from .engine import engine


def read_crop(page, box):
    image = page["clean_image"]
    width, height = page["size"]
    x1, y1, x2, y2 = np.asarray(box) * [width, height, width, height]
    x1, x2 = max(0, int(x1)), min(width, int(x2))
    y1, y2 = max(0, int(y1)), min(height, int(y2))
    crop = image[y1:y2, x1:x2]
    if not crop.size or min(crop.shape[:2]) < 5 or crop.shape[0] > 100:
        return []
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    if np.mean(gray < 130) < .015:
        return []
    result, _ = engine()(crop, use_det=False, use_cls=False)
    if not result:
        return []
    text, score = result[0]
    if score < .9 or len(re.sub(r"\W", "", text)) < 2:
        return []
    return [{"text": text, "score": float(score),
             "polygon": [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]}]
