GROUPS = [
    ("identity", "Provider & claim", [1, 2, 3, 4, 5, 56, 57]),
    ("patient", "Patient demographics", [8, 9, 10, 11]),
    ("admission", "Statement & admission", [6, 12, 13, 14, 15, 16, 17]),
    ("conditions", "Conditions & occurrences", list(range(18, 30)) + list(range(31, 37))),
    ("values", "Responsible party & values", [38, 39, 40, 41]),
    ("services", "Service lines & charges", list(range(42, 49))),
    ("coverage", "Payers & coverage", list(range(50, 56)) + list(range(58, 66))),
    ("clinical", "Diagnoses & procedures", list(range(66, 75))),
    ("providers", "Clinical providers", [76, 77, 78, 79]),
    ("remarks", "Remarks & additional codes", [80, 81]),
    ("reserved", "Reserved positions", [7, 30, 37, 49, 75]),
]
LABELS = {
    1: "Billing provider", 2: "Pay-to address", 3: "Patient control / medical record",
    4: "Type of bill", 5: "Tax identifier", 6: "Statement period", 8: "Patient name",
    9: "Patient address", 10: "Birth date", 11: "Sex", 12: "Admission date",
    13: "Admission hour", 14: "Admission priority", 15: "Admission origin",
    16: "Discharge hour", 17: "Discharge status", 29: "Accident state",
    38: "Responsible party", 42: "Revenue code", 43: "Service description",
    44: "Procedure / rate code", 45: "Service date", 46: "Units",
    47: "Charges", 48: "Noncovered charges", 50: "Payer", 51: "Plan identifier",
    52: "Release of information", 53: "Assignment of benefits", 54: "Prior payments",
    55: "Estimated amount due", 56: "Billing provider NPI", 57: "Other provider ID",
    58: "Insured name", 59: "Patient relationship", 60: "Insured identifier",
    61: "Group name", 62: "Group number", 63: "Authorization",
    64: "Document control number", 65: "Employer", 66: "Diagnosis qualifier",
    67: "Principal / other diagnoses", 68: "Unlabeled diagnosis area",
    69: "Admitting diagnosis", 70: "Patient reason for visit", 71: "PPS code",
    72: "External cause", 73: "Unlabeled", 74: "Procedure codes and dates",
    76: "Attending provider", 77: "Operating provider", 78: "Other provider 1",
    79: "Other provider 2", 80: "Remarks", 81: "Additional qualified codes",
}


def label(locator):
    if 18 <= locator <= 28:
        return "Condition code"
    if 31 <= locator <= 34:
        return "Occurrence code and date"
    if locator in (35, 36):
        return "Occurrence span"
    if 39 <= locator <= 41:
        return "Value code and amount"
    return LABELS.get(locator, "Reserved / unlabeled")


def groups():
    return [{"id": key, "label": title, "locators": locs} for key, title, locs in GROUPS]
