"""Install a project-local Node runtime; no changes to the system PATH."""
import io
import urllib.request
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1] / ".runtime"
root.mkdir(exist_ok=True)
version = "v22.16.0"
url = f"https://nodejs.org/dist/{version}/node-{version}-win-x64.zip"
with urllib.request.urlopen(url, timeout=60) as response:
    payload = response.read()
with zipfile.ZipFile(io.BytesIO(payload)) as archive:
    archive.extractall(root)
print(root / f"node-{version}-win-x64")
