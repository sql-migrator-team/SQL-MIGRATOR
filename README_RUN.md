# Running SQL-MIGRATOR locally

Options to run the backend API locally or with Docker.

1) Using a Python virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

Then open http://localhost:8000 in your browser (or POST to `/convert`).

2) Using Docker

```bash
docker build -t sql-migrator:latest .
docker run -p 8000:8000 sql-migrator:latest
```

Notes:
- If you install packages system-wide, you may need `sudo` on some systems.
- The repository contains a simple `converter` sample you can run with `python3 backend/converter.py`.
