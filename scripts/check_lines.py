"""Enforce the user's strict authored-file size requirement."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", ".runtime", "node_modules", "data", "dist",
            "__pycache__", ".pytest_cache", "test-results", ".uv-cache"}
GENERATED = {"package-lock.json"}
TEXT = {".py", ".ts", ".tsx", ".css", ".md", ".json", ".txt", ".sh", ".toml",
        ".csv", ".ps1", ".nix", ".js", ".mjs"}


def check():
    failures, counted = [], 0
    paths = []
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [name for name in subdirectories if name not in EXCLUDED]
        paths.extend(Path(directory) / name for name in filenames)
    for path in paths:
        if not path.is_file() or any(part in EXCLUDED for part in path.parts):
            continue
        if path.name in GENERATED or path.suffix not in TEXT:
            continue
        try:
            lines = len(path.read_text(encoding="utf-8-sig").splitlines())
        except UnicodeDecodeError:
            continue
        counted += 1
        if lines >= 100:
            failures.append(f"{path.relative_to(ROOT)}: {lines} lines")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {counted} authored/result files have fewer than 100 lines.")
    print("Excluded: dependencies, runtime data, build output, generated npm lockfile.")


if __name__ == "__main__":
    check()
