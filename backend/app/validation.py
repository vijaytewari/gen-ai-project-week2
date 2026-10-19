from datetime import date
from decimal import Decimal, InvalidOperation


def validate(claim):
    from .extraction.validation import review_issues, professional_issues
    lookup = {f["id"]: f for f in claim["fields"]}
    schema_issues = [{**error, "group": lookup[error["field_id"]]["group"]}
                     for error in claim.get("schema_validation", {}).get("errors", [])
                     if error["field_id"] in lookup]
    if claim.get("form_type") == "CMS-1500":
        return professional_issues(claim) + schema_issues
    fields = {f["id"]: f for f in claim["fields"]}
    issues = review_issues(claim) + schema_issues
    def issue(key, message):
        issues.append({"field_id": key, "group": fields[key]["group"], "message": message})
    for key, field in fields.items():
        if field["status"] == "unreadable":
            issue(key, "Unreadable value needs manual review")
        value = field["value"]
        is_date = key in ("10", "12", "6.from", "6.through", "31.date", "74.date")
        is_date = is_date or key.startswith("45.")
        if value and is_date:
            try:
                date.fromisoformat(value)
            except ValueError:
                issue(key, "Use a valid YYYY-MM-DD date")
        if value and field["locator"] in (46, 47, 48, 54, 55):
            try:
                number = Decimal(value)
                if not number.is_finite() or number < 0:
                    raise InvalidOperation
            except InvalidOperation:
                issue(key, "Use a finite nonnegative number")
    start, end = fields["6.from"]["value"], fields["6.through"]["value"]
    if start and end and start > end:
        issue("6.through", "Statement end precedes statement start")
    try:
        total = fields["47.total"]["value"]
        lines = [f["value"] for f in fields.values()
                 if f["locator"] == 47 and f["id"] != "47.total"]
        if total and all(lines) and Decimal(total) != sum(map(Decimal, lines)):
            issue("47.total", "Total does not equal the sum of line charges")
    except InvalidOperation:
        pass
    return issues
