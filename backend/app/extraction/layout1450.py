"""Value windows for the standard institutional layout; no grid detection required."""
SCALARS = {
    "1": (.043, .051, .318, .103), "2": (.322, .058, .594, .103),
    "3.a": (.598, .052, .895, .065), "3.b": (.598, .067, .895, .079),
    "4": (.898, .062, .952, .079), "5": (.598, .088, .707, .104),
    "6.from": (.712, .093, .785, .105), "6.through": (.789, .093, .862, .105),
    "8": (.044, .118, .373, .134), "9": (.378, .11, .951, .147),
    "10": (.044, .147, .138, .161), "11": (.144, .147, .173, .161),
    "12": (.178, .147, .239, .161), "13": (.244, .147, .271, .161),
    "14": (.275, .147, .305, .161), "15": (.309, .147, .339, .161),
    "16": (.343, .147, .371, .161), "17": (.375, .147, .406, .161),
    "29": (.776, .147, .808, .161), "38": (.044, .218, .515, .27),
    "47.total": (.704, .594, .814, .605), "56": (.755, .62, .951, .633),
    "57": (.755, .637, .951, .662), "66": (.043, .781, .056, .798),
    "67.principal": (.059, .78, .141, .799), "67.other1": (.144, .78, .23, .799),
    "69": (.044, .811, .162, .825), "70": (.167, .811, .44, .825),
    "71": (.442, .811, .52, .825), "72": (.525, .811, .84, .825),
    "74.code": (.044, .837, .15, .852), "74.date": (.153, .837, .228, .852),
    "76": (.602, .824, .951, .86), "77": (.602, .862, .951, .886),
    "78": (.602, .89, .951, .914), "79": (.602, .918, .951, .94),
    "80": (.044, .881, .308, .924), "81": (.313, .881, .595, .924),
}


def window(field, synthetic=False):
    if synthetic:
        from ..fixtures import fields
        from ..form_layout import field_box
        siblings = [f for f in fields(empty=True) if f["locator"] == field["locator"]]
        if field["id"] not in {f["id"] for f in siblings}:
            return None
        sibling = next(f for f in siblings if f["id"] == field["id"])
        x, y, width, height = field_box(sibling, siblings)
        return (x / 850, (y + 6) / 1100, (x + width) / 850, (y + height) / 1100)
    key, loc = field["id"], field["locator"]
    if key in SCALARS:
        return SCALARS[key]
    if 18 <= loc <= 28:
        left = .409 + (loc - 18) * .033
        return (left, .147, left + .031, .161)
    if 42 <= loc <= 48:
        edges = [.043, .093, .369, .536, .615, .703, .814, .924]
        row = (int(field["row"]) - 1) % 22
        return (edges[loc - 42], .286 + row * .014, edges[loc - 41], .299 + row * .014)
    if 50 <= loc <= 55:
        edges = [.043, .297, .463, .485, .505, .629, .75]
        row = "ABC".index(key[-1])
        return (edges[loc - 50], .62 + row * .014, edges[loc - 49], .633 + row * .014)
    if 58 <= loc <= 62:
        edges = [.043, .33, .365, .585, .752, .951]
        row = "ABC".index(key[-1])
        return (edges[loc - 58], .676 + row * .014, edges[loc - 57], .689 + row * .014)
    if 63 <= loc <= 65:
        edges = [.043, .385, .675, .951]
        row = "ABC".index(key[-1])
        return (edges[loc - 63], .732 + row * .014, edges[loc - 62], .745 + row * .014)
    return None
