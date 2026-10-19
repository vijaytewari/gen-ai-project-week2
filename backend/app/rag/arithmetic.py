from decimal import Decimal, InvalidOperation


def calculate(claim, query, hits):
    text = query.lower()
    if not (any(word in text for word in ("sum", "calculate")) and "charges" in text):
        return None
    locator = 48 if "noncovered" in text or "non-covered" in text else 47
    fields = [f for f in claim["fields"] if f["locator"] == locator and f["row"] != "total"]
    allowed = {key for hit in hits for key in hit["document"].metadata["field_ids"]}
    if not fields or any(f["id"] not in allowed or f["status"] != "present" for f in fields):
        return {"answer": "Insufficient evidence to sum every service line.",
                "citations": [], "abstained": True, "mode": "calculation"}
    try:
        amounts = [Decimal(f["value"]) for f in fields]
        if any(not number.is_finite() or number < 0 for number in amounts):
            raise InvalidOperation
    except InvalidOperation as exc:
        raise ValueError("Resolve invalid charges before calculating") from exc
    return {"answer": f"Sum of {'noncovered ' if locator == 48 else ''}line charges: {sum(amounts):.2f}",
            "abstained": False, "mode": "calculation", "citations": [
                {"field_id": f["id"], "label": f["label"], "value": f["value"],
                 "group": f["group"], "evidence": f["evidence"], "source": f["source"]}
                for f in fields]}
