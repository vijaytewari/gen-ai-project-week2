#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements.txt
npm --prefix frontend ci
npm --prefix frontend run build
exec python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
