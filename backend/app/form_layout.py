"""Original synthetic layout organized like a claim, not a billing form."""


def base_box(loc):
    top = {1: (20, 45, 245, 60), 2: (265, 45, 245, 60), 3: (510, 45, 210, 30),
           4: (720, 45, 110, 30), 5: (510, 75, 115, 30), 6: (625, 75, 165, 30),
           7: (790, 75, 40, 30), 8: (20, 105, 290, 38), 9: (310, 105, 520, 38),
           10: (20, 143, 90, 35), 11: (110, 143, 38, 35), 12: (148, 143, 85, 35),
           13: (233, 143, 35, 35), 14: (268, 143, 35, 35), 15: (303, 143, 35, 35),
           16: (338, 143, 35, 35), 17: (373, 143, 40, 35),
           29: (752, 143, 38, 35), 30: (790, 143, 40, 35),
           35: (420, 178, 185, 55), 36: (605, 178, 185, 55), 37: (790, 178, 40, 55),
           38: (20, 233, 400, 80), 39: (420, 233, 137, 80),
           40: (557, 233, 137, 80), 41: (694, 233, 136, 80),
           56: (700, 600, 130, 30), 57: (700, 630, 130, 60),
           66: (20, 830, 35, 40), 67: (55, 830, 710, 40), 68: (765, 830, 65, 40),
           74: (20, 910, 450, 55), 75: (470, 910, 40, 55),
           80: (20, 965, 260, 65), 81: (280, 965, 230, 65)}
    if loc in top:
        return top[loc]
    if 18 <= loc <= 28:
        return (413 + (loc - 18) * 30.8, 143, 30.8, 35)
    if 31 <= loc <= 34:
        return (20 + (loc - 31) * 100, 178, 100, 55)
    if 42 <= loc <= 48:
        edges = [20, 65, 310, 460, 535, 610, 720, 830]
        n = loc - 42
        return (edges[n], 330, edges[n + 1] - edges[n], 250)
    if loc == 49:
        return (810, 580, 20, 20)
    if 50 <= loc <= 55:
        edges = [20, 255, 390, 430, 470, 580, 700]
        n = loc - 50
        return (edges[n], 600, edges[n + 1] - edges[n], 90)
    if 58 <= loc <= 62:
        edges = [20, 260, 300, 500, 660, 830]
        n = loc - 58
        return (edges[n], 700, edges[n + 1] - edges[n], 60)
    if 63 <= loc <= 65:
        return (20 + (loc - 63) * 270, 770, 270, 50)
    if 69 <= loc <= 73:
        return (20 + (loc - 69) * 162, 870, 162, 40)
    if 76 <= loc <= 79:
        return (510, 910 + (loc - 76) * 30, 320, 30)
    raise ValueError(f"Unmapped locator {loc}")


def field_box(field, siblings):
    x, y, width, height = base_box(field["locator"])
    position = siblings.index(field)
    if 42 <= field["locator"] <= 48:
        if field["row"] == "total":
            return (x, y + height - 24, width, 24)
        return (x, y + position * 27, width, 27)
    if len(siblings) > 1:
        height /= len(siblings)
        y += position * height
    return (x, y, width, height)
