def values(case):
    name = ["Jordan Reed", "Avery Chen", "Morgan Ellis", "Taylor Brooks"][case % 4]
    charge = 1200 + case * 137
    return {
        "1": "DEMO Harbor Medical Center", "2": "100 Fictional Avenue, Demo City NY 00000",
        "3.a": f"DEMO-{case + 1:04d}", "3.b": f"MR-DEMO-{case + 1:04d}",
        "4": "0111", "5": "00-0000000", "6.from": "2026-09-10",
        "6.through": "2026-09-12", "8": name, "9": "42 Example Lane, Demo City NY 00000",
        "10": "1980-02-15", "11": "X", "12": "2026-09-10", "13": "09",
        "14": "1", "15": "1", "16": "14", "17": "01", "18": "DEMO",
        "31.code": "DEMO", "31.date": "2026-09-10", "38": name,
        "39.code": "DEMO", "39.amount": "100.00", "42.1": "0120",
        "43.1": "Room and board", "44.1": "DEMO-ROOM", "45.1": "2026-09-10",
        "46.1": "2", "47.1": f"{charge:.2f}", "48.1": "0.00", "42.2": "0300",
        "43.2": "Laboratory services", "44.2": "DEMO-LAB", "45.2": "2026-09-11",
        "46.2": "1", "47.2": "250.00", "48.2": "0.00",
        "47.total": f"{charge + 250:.2f}", "50.A": "DEMO Primary Health",
        "50.B": "DEMO Supplemental", "51.A": "PLAN-DEMO", "52.A": "Y", "53.A": "Y",
        "54.A": "100.00", "55.A": f"{charge + 150:.2f}", "56": "0000000000",
        "58.A": name, "59.A": "18", "60.A": f"SYNTHETIC-{case + 1:04d}",
        "61.A": "Demo group", "62.A": "GROUP-000", "63.A": "DEMO-AUTH",
        "64.A": f"DCN-DEMO-{case}", "65.A": "Fictional Employer", "66": "0",
        "67.principal": "DEMO-DX", "67.other1": "DEMO-SECONDARY",
        "69": "DEMO-ADMIT", "70": "Synthetic review encounter",
        "74.code": "DEMO-PROC", "74.date": "2026-09-11", "76": "Dr Example, DEMO-NPI",
        "77": "Dr Sample, DEMO-NPI", "80": "Synthetic claim for workflow testing only.",
        "81": "DEMO additional qualifier",
    }
