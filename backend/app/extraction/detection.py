import re


def detect(tokens):
    text = " ".join(t["text"] for t in tokens).upper()
    compact = re.sub(r"[^A-Z0-9]", "", text)
    professional = sum(term in compact for term in (
        "FORM1500", "CMS1500", "HEALTHINSURANCECLAIMFORM", "NUCC", "PATIENTSACCOUNT"))
    institutional = sum(term in compact for term in (
        "CMS1450", "UB04", "TYPEOFBILL", "STATEMENTCOVERS", "REVENUECODE", "NUBC"))
    revenue_codes = {t["text"].strip() for t in tokens
                     if re.fullmatch(r"0?\d{3}", t["text"].strip())}
    if "CREATIONDATE" in compact and "TOTALS" in compact and len(revenue_codes) >= 4:
        institutional += 1
    if professional > institutional and professional:
        return "CMS-1500", professional
    if institutional:
        return "CMS-1450", institutional
    return "unknown", 0
