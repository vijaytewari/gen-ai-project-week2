"""Optional grid fallback for photographed institutional forms with unreadable labels."""
import cv2
import numpy as np


def bands(indices):
    return [group for group in np.split(indices, np.where(np.diff(indices) > 1)[0] + 1)
            if len(group)]


def align_grid(page):
    image = page.get("image")
    if image is None:
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    ink = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)[1]
    vertical = cv2.morphologyEx(ink, cv2.MORPH_OPEN,
                               np.ones((max(20, height // 10), 1), np.uint8))
    column_ink = (vertical[int(.30 * height):int(.61 * height)] > 0).sum(axis=0)
    columns = np.flatnonzero(column_ink > height * .15)
    columns = np.array([group.mean() for group in bands(columns) if len(group) < width * .012])
    columns = columns[(columns > width * .005) & (columns < width * .97)]
    if not len(columns):
        return None
    left, right = int(columns.min()), int(columns.max())
    if not .75 < (right - left) / width < .97:
        return None
    horizontal = cv2.morphologyEx(ink, cv2.MORPH_OPEN,
                                 np.ones((1, max(20, width // 5)), np.uint8))
    rows = np.flatnonzero((horizontal[:, left:right] > 0).sum(axis=1) > (right - left) * .72)
    rows = rows[(rows > height * .045) & (rows < height * .97)]
    thin_rows = [group.mean() for group in bands(rows) if len(group) <= height * .006]
    if len(thin_rows) < 10:
        return None
    top, bottom = min(thin_rows) / height, max(thin_rows) / height
    dark = (gray[:, int(width * .1):int(width * .9)] < 70).mean(axis=1)
    footer = [group for group in bands(np.flatnonzero(dark > .9))
              if group[0] > height * .85 and len(group) >= height * .003]
    if footer:
        bottom = footer[0][0] / height
    if not .78 < bottom - top < .93:
        return None
    expected, observed = [], []
    for nominal in (.093, .369, .536, .615, .703, .814, .924, .952):
        candidate = min(columns / width, key=lambda x: abs(x - nominal))
        if abs(candidate - nominal) < .025:
            expected.append(nominal)
            observed.append(candidate)
    if len(expected) < 4:
        return None
    sx, tx = np.polyfit(expected, observed, 1)
    if not .9 < sx < 1.1:
        return None
    sy = (bottom - top) / .875
    return np.array([[sx, 0, tx], [0, sy, top - sy * .05]])
