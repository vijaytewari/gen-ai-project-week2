from backend.app.fixture_values import values

TEMPLATES = [
    ("What is the patient name?", ["8"]),
    ("What is the statement period?", ["6.from", "6.through"]),
    ("What are the total charges?", ["47.total"]),
    ("What is the primary payer?", ["50.A"]),
    ("What is the patient's bank account number?", []),
]


def queries():
    result = []
    for case in range(12):
        for number, (text, gold) in enumerate(TEMPLATES):
            if number == 3 and case % 3 == 1:
                text, gold = "What is the principal diagnosis?", ["67.principal"]
            if number == 3 and case % 3 == 2:
                text, gold = "What are the admission date and discharge status?", ["12", "17"]
            result.append({"id": f"case-{case:02d}-q{number}", "case": case,
                "query": text, "gold": gold, "expected": {k: values(case)[k] for k in gold},
                "split": "development" if case < 3 else "heldout",
                "category": ["identity", "dates", "amount", "coverage-or-clinical", "unanswerable"][number]})
    return result
