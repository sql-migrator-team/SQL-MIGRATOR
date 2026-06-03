**Frontend Integration Notes**

This document lists the minimal changes your frontend needs to make to work with the updated backend in this repository.

Summary of backend changes
- **CORS enabled** for common local origins. The API accepts requests from `http://localhost`, `http://127.0.0.1` and ports like `3000`.
- Static files are mounted at `/static` (optional).
- Endpoints available:
  - `POST /convert` — multipart file upload (`file` form field). Optional form fields: `source_db`, `target_db`.
  - `POST /convert_text` — JSON body: `{ sql_text, source_db, target_db }` for converting text directly.
  - `GET /health` — health check.

Required frontend changes
- Ensure the frontend sends requests to the correct backend origin, e.g. `http://localhost:8000`.
- Use a file upload form that posts to `/convert` using `fetch` + `FormData`.
- Optionally provide a textarea + button that sends JSON to `/convert_text`.

Recommended HTML element IDs (examples)
- File input: `sqlFile` (type="file")
- Source DB select: `sourceDb` (e.g. mysql)
- Target DB select: `targetDb` (e.g. postgresql)
- Convert button: `convertBtn`
- Textarea for SQL input: `sqlText`
- Result container: `convertedSql`
- Validation container: `validation`
- Report container: `report`

Sample JavaScript for file upload (replace or add to `frontend/js/script.js`):

```javascript
async function uploadAndConvert() {
  const fileInput = document.getElementById('sqlFile');
  const source = document.getElementById('sourceDb').value || 'mysql';
  const target = document.getElementById('targetDb').value || 'postgresql';

  if (!fileInput.files.length) {
    alert('Select a SQL file first');
    return;
  }

  const form = new FormData();
  form.append('file', fileInput.files[0]);
  form.append('source_db', source);
  form.append('target_db', target);

  const res = await fetch('http://localhost:8000/convert', {
    method: 'POST',
    body: form,
  });

  const data = await res.json();
  if (res.ok) {
    document.getElementById('convertedSql').textContent = data.converted_sql;
    document.getElementById('validation').textContent = JSON.stringify(data.validation, null, 2);
    document.getElementById('report').textContent = JSON.stringify(data.report, null, 2);
  } else {
    alert('Error: ' + (data.detail || data.message || JSON.stringify(data)));
  }
}

document.getElementById('convertBtn').addEventListener('click', uploadAndConvert);
```

Sample JavaScript for text conversion (useful for textarea):

```javascript
async function convertText() {
  const sql = document.getElementById('sqlText').value;
  const source = document.getElementById('sourceDb').value || 'mysql';
  const target = document.getElementById('targetDb').value || 'postgresql';

  const res = await fetch('http://localhost:8000/convert_text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sql_text: sql, source_db: source, target_db: target }),
  });

  const data = await res.json();
  if (res.ok) {
    document.getElementById('convertedSql').textContent = data.converted_sql;
    document.getElementById('validation').textContent = JSON.stringify(data.validation, null, 2);
    document.getElementById('report').textContent = JSON.stringify(data.report, null, 2);
  } else {
    alert('Error: ' + (data.detail || data.message || JSON.stringify(data)));
  }
}

// Hook a button with id `convertTextBtn` to call convertText()
```

Notes and tips
- If you serve the frontend from a different host/port, add that origin to the `allow_origins` list in `backend/main.py`.
- The backend returns `validation` as a `ValidationResult` object (serialized by FastAPI). Use `JSON.stringify()` to inspect.
- To serve the frontend from the backend, place the built frontend files in the `frontend/` folder and request static assets at `/static/`.

If you want, I can:
- Add example form markup to `frontend/converter.html` and wire it to `frontend/js/script.js`.
- Add CORS wildcard for quick testing (not recommended for production).
## Frontend change checklist (from -> to)

- `fetch('/convert')` -> `fetch('http://localhost:8000/convert')`
- `fetch('/convert_text')` -> `fetch('http://localhost:8000/convert_text')`
- file input name `sql` or custom name -> `file` in `FormData`
- source DB form field name `sourceDb` or custom name -> `source_db`
- target DB form field name `targetDb` or custom name -> `target_db`
- text conversion JSON field `sql` or custom name -> `sql_text`
- direct textarea-only form -> `POST` JSON body with `Content-Type: application/json`
- frontend file upload form -> `multipart/form-data` request body using `FormData`
- static file references from `frontend/...` to backend-served `/static/...` if you want the backend to serve the UI
- local frontend origin `file://` or another port -> add that origin to `allow_origins` in `backend/main.py`
- result display area `output` or other id -> `convertedSql`/`validation`/`report` as recommended IDs for example script wiring