from functools import lru_cache
import cv2
import numpy as np


@lru_cache(maxsize=1)
def engine():
    from rapidocr_onnxruntime import RapidOCR
    return RapidOCR(intra_op_num_threads=2, inter_op_num_threads=1,
                    det_limit_side_len=1600, det_limit_type="max", max_side_len=2400,
                    rec_batch_num=8)


def recognize(image):
    result, _ = engine()(image)
    return [{"text": str(text), "score": float(score), "polygon": np.asarray(box).tolist()}
            for box, text, score in (result or [])]


def without_red(image):
    blue, green, red = cv2.split(image)
    mask = (red.astype(float) > green * 1.1) & (red.astype(float) > blue * 1.1) & (red > 100)
    output = image.copy()
    output[mask] = 255
    return output
