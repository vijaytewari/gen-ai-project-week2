import re
from ..config import setting
from .arithmetic import calculate

STOP = {"what", "is", "the", "for", "this", "claim", "please", "show", "me", "are",
        "a", "an", "of", "and", "does", "have", "which", "was", "in", "on", "to"}


def select_fields(claim, query, hits):
    allowed = {key for h in hits for key in h["document"].metadata["field_ids"]}
    terms = set(re.findall(r"[a-z0-9]+", query.lower())) - STOP
    candidates = []
    for field in claim["fields"]:
        if field["id"] not in allowed or field["status"] != "present" or not field["value"]:
            continue
        tokens = set(re.findall(r"[a-z0-9]+", field["label"].lower()))
        score = len(tokens & terms) / max(len(terms), 1)
        if score >= 0.5:
            candidates.append((score, field))
    candidates.sort(key=lambda item: (-item[0], item[1]["id"]))
    best = candidates[0][0] if candidates else 0
    return [f for score, f in candidates if score == best][:5]


def answer(claim, query, hits):
    calculation = calculate(claim, query, hits)
    if calculation is not None:
        return calculation
    fields = select_fields(claim, query, hits)
    citations = [{"field_id": f["id"], "label": f["label"], "value": f["value"],
                  "group": f["group"], "evidence": f["evidence"], "source": f["source"]}
                 for f in fields]
    if not fields:
        return {"answer": "Insufficient evidence in this claim to answer that question.",
                "citations": [], "abstained": True, "mode": "lookup"}
    if setting("ANSWER_MODE", "lookup") == "llm":
        from .generation import generate
        return generate(query, citations)
    text = "\n".join(f"{f['label']}: {f['value']} [FL {f['id']}]" for f in fields)
    return {"answer": text, "citations": citations, "abstained": False, "mode": "lookup"}
