from langchain_core.documents import Document


def canonical(claim):
    text, spans = "", []
    ordered = list(claim["fields"])
    service = sorted((f for f in ordered if f["group"] == "services"),
                     key=lambda f: (f["row"] == "total", f["row"], f["locator"]))
    iterator = iter(service)
    ordered = [next(iterator) if f["group"] == "services" else f for f in ordered]
    for field in ordered:
        if field["status"] != "present" or not field["value"]:
            continue
        line = (f"[{field['group']}] FL {field['id']} {field['label']}: "
                f"{field['value']}\n")
        spans.append({"id": field["id"], "group": field["group"], "row": field["row"], "start": len(text),
                      "end": len(text) + len(line), "evidence": field["evidence"]})
        text += line
    return Document(page_content=text, metadata={"claim_id": claim["id"],
                    "revision": claim["revision"], "spans": spans})
