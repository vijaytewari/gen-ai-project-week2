import csv
import json
from pathlib import Path


def write_json(path, value):
    """Generated JSON is paged into small artifacts, not one giant results file."""
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_rows(path, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_evidence(folder, number, evidence):
    target = folder / f"query-{number:02d}"
    target.mkdir()
    write_json(target / "query.json", evidence["query"])
    response = evidence["answer"]
    write_json(target / "answer.json", {k: v for k, v in response.items() if k != "citations"})
    for n, citation in enumerate(response["citations"]):
        write_json(target / f"citation-{n}.json", citation)
    for n, candidate in enumerate(evidence["candidates"]):
        write_json(target / f"candidate-{n:02d}.json", candidate)
