"""Professional-claim fields; these IDs never reuse CMS1450 locator meanings."""
GROUPS = [
    ("identity", "Billing provider & totals", [25, 26, 28, 29, 33]),
    ("patient", "Patient demographics", [2, 3, 5]),
    ("coverage", "Insured & coverage", [1, 4, 7, 9, 11]),
    ("clinical", "Diagnoses & authorization", [19, 21, 23]),
    ("services", "Professional service lines", [24]),
    ("providers", "Providers & signatures", [12, 13, 17, 31, 32]),
]
# Boxes describe value areas on the standard page, not required grid lines.
SCALARS = [
    ("1a", "Insured identifier", "coverage", (.602, .138, .95, .158)),
    ("2", "Patient name", "patient", (.038, .167, .367, .187)),
    ("3", "Patient birth date", "patient", (.38, .167, .515, .187)),
    ("5.street", "Patient street", "patient", (.038, .195, .367, .22)),
    ("5.city", "Patient city", "patient", (.038, .227, .32, .248)),
    ("5.state", "Patient state", "patient", (.328, .227, .367, .248)),
    ("5.zip", "Patient ZIP", "patient", (.038, .258, .18, .28)),
    ("5.phone", "Patient phone", "patient", (.19, .258, .367, .28)),
    ("4", "Insured name", "coverage", (.602, .167, .95, .187)),
    ("7.street", "Insured street", "coverage", (.602, .195, .95, .22)),
    ("7.city", "Insured city", "coverage", (.602, .227, .87, .248)),
    ("7.state", "Insured state", "coverage", (.875, .227, .95, .248)),
    ("7.zip", "Insured ZIP", "coverage", (.602, .258, .75, .28)),
    ("7.phone", "Insured phone", "coverage", (.76, .258, .95, .28)),
    ("9", "Other insured name", "coverage", (.038, .285, .367, .308)),
    ("9a", "Other insured identifier", "coverage", (.038, .315, .367, .338)),
    ("9d", "Other plan name", "coverage", (.038, .402, .367, .433)),
    ("11", "Insured policy group", "coverage", (.602, .285, .95, .309)),
    ("11a", "Insured birth date", "coverage", (.625, .314, .79, .34)),
    ("11c", "Insurance plan name", "coverage", (.602, .372, .95, .397)),
    ("12", "Patient signature", "providers", (.038, .46, .385, .483)),
    ("12.date", "Patient signature date", "providers", (.393, .46, .59, .483)),
    ("13", "Insured signature", "providers", (.602, .46, .95, .483)),
    ("17", "Referring provider", "providers", (.038, .518, .339, .543)),
    ("19", "Additional claim information", "clinical", (.038, .551, .59, .576)),
    ("21.A", "Diagnosis A", "clinical", (.055, .58, .18, .605)),
    ("21.B", "Diagnosis B", "clinical", (.18, .58, .31, .605)),
    ("23", "Authorization", "clinical", (.602, .616, .95, .632)),
    ("25", "Tax identifier", "identity", (.038, .851, .285, .869)),
    ("26", "Patient account", "identity", (.29, .851, .45, .869)),
    ("28", "Total charges", "identity", (.605, .851, .738, .869)),
    ("29", "Amount paid", "identity", (.744, .851, .843, .869)),
    ("31", "Physician signature", "providers", (.038, .883, .28, .942)),
    ("32", "Service facility", "providers", (.29, .878, .594, .945)),
    ("33", "Billing provider", "identity", (.602, .878, .95, .945)),
]
SERVICE_COLUMNS = [
    ("date", "Service date", .04, .27), ("place", "Place of service", .27, .33),
    ("procedure", "Procedure code", .37, .455), ("modifier", "Modifier", .455, .505),
    ("diagnosis", "Diagnosis pointer", .565, .625), ("charges", "Line charges", .63, .711),
    ("units", "Units", .715, .76), ("provider", "Rendering provider", .811, .95),
]


def definitions():
    items = list(SCALARS)
    for row in range(1, 7):
        top = .671 + (row - 1) * .0295
        for key, title, left, right in SERVICE_COLUMNS:
            items.append((f"24.{row}.{key}", f"{title} · row {row}", "services",
                          (left, top, right, top + .022)))
    return items


def groups():
    return [{"id": key, "label": title, "locators": locators} for key, title, locators in GROUPS]
