import cv2
import numpy as np


def rotate(image, angle):
    height, width = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    cos, sin = abs(matrix[0, 0]), abs(matrix[0, 1])
    new_width, new_height = int(height * sin + width * cos), int(height * cos + width * sin)
    matrix[:, 2] += [(new_width - width) / 2, (new_height - height) / 2]
    output = cv2.warpAffine(image, matrix, (new_width, new_height), borderValue=(255, 255, 255))
    return output, np.vstack([matrix, [0, 0, 1]])


def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 180)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 1800, 100,
                            minLineLength=image.shape[1] // 5, maxLineGap=20)
    angles = []
    for x1, y1, x2, y2 in [] if lines is None else lines.reshape(-1, 4):
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle) < 12:
            angles.append(angle)
    angle = float(np.median(angles)) if angles else 0
    if abs(angle) < .25:
        return image, np.eye(3), 0.0
    corrected, matrix = rotate(image, angle)
    return corrected, matrix, angle


def evidence(tokens, inverse, original_size, page, pdf_rotation):
    points = np.concatenate([np.asarray(t["polygon"]) for t in tokens])
    points = np.column_stack([points, np.ones(len(points))]) @ inverse.T
    width, height = original_size
    points = points[:, :2] / [width, height]
    if pdf_rotation == 90:
        points = np.column_stack([points[:, 1], 1 - points[:, 0]])
    elif pdf_rotation == 180:
        points = 1 - points
    elif pdf_rotation == 270:
        points = np.column_stack([1 - points[:, 1], points[:, 0]])
    points = np.clip(points, 0, 1)
    left, top = points.min(axis=0)
    right, bottom = points.max(axis=0)
    return {"page": page, "box": [float(left), float(top), float(right-left), float(bottom-top)]}
