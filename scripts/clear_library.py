"""Explicit maintenance command: clear library claims and generated JSON files."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.app import database as db
from backend.app.config import DATA


def clear():
    db.initialize()
    with db.connection() as connection:
        count = connection.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
        for table in ("saved_json", "claims", "history", "audit", "jobs"):
            connection.execute(f"DELETE FROM {table}")
    root = DATA.resolve()
    directory = (root / "json").resolve()
    if not directory.is_relative_to(root):
        raise ValueError("JSON directory is outside the data directory")
    removed = 0
    for path in directory.glob("*.json"):
        if not path.resolve().is_relative_to(directory):
            raise ValueError("Snapshot path is outside the JSON directory")
        path.unlink()
        removed += 1
    print(f"Cleared {count} claims and {removed} generated JSON files. Source originals retained.")


if __name__ == "__main__":
    clear()
