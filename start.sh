#!/usr/bin/env bash
set -euo pipefail

# Go to backend
cd backend

# Install dependencies (use pip cache on Railway if available)
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run migrations/create tables (safe for assignment)
python - <<'PY'
from backend import main as m
# main.py already calls Base.metadata.create_all(bind=...) so just import ensures table exists
print("DB initialized (if reachable).")
PY

# Start uvicorn using environment PORT variable provided by Railway
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
