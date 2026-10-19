import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=False)
except ImportError:
    pass
DATA = Path(os.getenv("DATA_DIR", str(ROOT / "data")))
DATA.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(DATA / "models"))
os.environ.setdefault("LANGSMITH_TRACING", "false")
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
FILES = DATA / "files"
FILES.mkdir(exist_ok=True)
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)
MAX_BYTES = 20 * 1024 * 1024
MAX_PAGES = 9


def setting(name, default=""):
    return os.getenv(name, default)
