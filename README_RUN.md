# Running SQL-MIGRATOR locally

This document shows how to run SQL-MIGRATOR from the repository base directory.

## Prerequisites

- Python 3.10+ installed
- `pip` available
- `git` (optional)
- Docker installed if you want to use the Docker option

## Recommended local run (Python virtual environment)

1. Open a terminal and change to the repository root:

```bash
cd /home/ark/Downloads/SQL-MIGRATOR-main
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Upgrade pip:

```bash
pip install --upgrade pip
```

4. Install required Python packages.

If a `requirements.txt` file exists, use:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt`, install the packages directly:

```bash
pip install fastapi uvicorn python-multipart
```

5. Start the backend service from the repository root:

```bash
uvicorn backend.main:app --reload --port 8000
```

6. Verify the backend is running by opening this URL in your browser:

```text
http://localhost:8000/health
```

You should see a JSON response like:

```json
{ "status": "running" }
```

## Accessing the frontend

The backend serves API routes only. To use the frontend pages, open one of the HTML files directly in your browser, for example:

```text
frontend/schema_generator.html
```

Or, if you want to use the backend API from a browser, open the HTML file and use the front-end forms to call the API.

## Frontend creation verification procedure

When creating or updating the frontend, follow these checks step by step:

1. Verify backend URL targets.
   - Use `http://localhost:8000/convert` for file upload requests.
   - Use `http://localhost:8000/convert_text` for JSON text conversions.

2. Confirm request formats.
   - File uploads must use `FormData` with field `file`.
   - Text conversions must use a JSON body with `sql_text`.
   - Set `Content-Type: application/json` for JSON requests.

3. Match frontend field names to backend parameters.
   - `file` in `FormData` for uploaded SQL files.
   - `source_db` for source database selection.
   - `target_db` for target database selection.
   - `sql_text` for plain SQL text payloads.

4. Validate HTML IDs and wiring.
   - Recommended IDs: `sqlFile`, `sourceDb`, `targetDb`, `convertBtn`, `sqlText`, `convertedSql`, `validation`, `report`.
   - Make sure JavaScript uses the exact ID values from your HTML.

5. Confirm CORS support.
   - If the frontend is served from a different origin, add that origin to `allow_origins` in `backend/main.py`.
   - Prefer using a local HTTP server (for example `python3 -m http.server 8080` from `frontend/`) instead of `file://`.

6. Test the backend health endpoint.
   - Open `http://localhost:8000/health` to ensure the backend is running.

7. Test conversion flows.
   - Upload a SQL file and verify the response contains `converted_sql`, `validation`, and `report`.
   - Submit text via textarea and verify output and validation display.

8. Inspect error handling.
   - Show API errors clearly in the UI.
   - Display `data.detail`, `data.message`, or raw JSON when the backend returns an error.

9. Check static asset usage.
   - If serving UI through the backend, reference assets under `/static/...`.
   - If opening HTML files directly, use relative paths inside `frontend/`.

10. Final production sanity checks.
   - Do not enable broad CORS wildcards in production.
   - Keep the allowed frontend origins explicit for local development.



## Example run from base

1. `cd /home/ark/Downloads/SQL-MIGRATOR-main`
2. `source .venv/bin/activate`
3. `uvicorn backend.main:app --reload --port 8000`
4. Open `frontend/schema_generator.html` in a browser

## Docker run

From the repository root:

```bash
docker build -t sql-migrator:latest .
docker run -p 8000:8000 sql-migrator:latest
```

Then open:

```text
http://localhost:8000/health
```

## Optional sample converter script

From the repository base, you can also run the sample converter directly:

```bash
python3 backend/converter.py
```

## Notes

- If you use a virtual environment, make sure it is active before running `uvicorn`.
- If you open HTML files directly, the browser may require the backend to be running for API-enabled features.
- If you need to add missing dependencies, install `fastapi`, `uvicorn`, and `python-multipart`.
