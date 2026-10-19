"""Write small, reviewable fixture and query manifests."""
import hashlib
import json
from pathlib import Path
from backend.app.fixtures import samples
from backend.app.source_pdf import create_sample
from evaluation.dataset import queries

ROOT = Path(__file__).resolve().parents[1] / "fixtures"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    for sample in samples():
        path, fields = create_sample(sample["id"])
        write(ROOT / "cases" / f"case-{sample['id']:02d}.json", {
            **sample, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "filename": path.name, "field_count": len(fields),
            "page_count": 1 + max(f["evidence"]["page"] for f in fields),
            "coordinate_units": "normalized original page; rotation applied by viewer",
            "extraction": "curated simulation", "layout": "original synthetic, not for billing"})
    for query in queries():
        write(ROOT / "queries" / f"{query['id']}.json", query)
    print("Exported 12 case manifests and 60 query judgments")
