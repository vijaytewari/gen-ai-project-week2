"""Retrieve a reference-only CMS form; never bundle it into demo output."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import fitz

URL = "https://www.reginfo.gov/public/do/DownloadDocument?objectID=83037001"
ROOT = Path(__file__).resolve().parents[1]


def fetch():
    directory = ROOT / "data" / "reference"
    directory.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(URL, headers={"User-Agent": "CMS1450-research-demo/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    target = directory / "cms1450-reference.pdf"
    target.write_bytes(payload)
    with fitz.open(target) as doc:
        first = doc[0]
        first.get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(directory / "reference-page.png")
        manifest = {"url": URL, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                    "sha256": hashlib.sha256(payload).hexdigest(), "pages": len(doc),
                    "first_page_excerpt": first.get_text()[:1000],
                    "usage": "Historical reference only; excluded from redistribution",
                    "demo_layout": "Original synthetic layout, not an official billing form"}
    (ROOT / "fixtures").mkdir(exist_ok=True)
    (ROOT / "fixtures" / "reference_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    fetch()
