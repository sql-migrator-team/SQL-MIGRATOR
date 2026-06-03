**Frontend Integration Notes**

This document lists the frontend state and the concrete changes needed for the current HTML pages in this repository.

Current frontend page status
- `frontend/admin.html` — empty placeholder. No admin UI content exists yet.
- `frontend/dashboard.html` — empty placeholder. No dashboard markup exists yet.
- `frontend/reports.html` — empty placeholder. No report UI exists yet.
- `frontend/login.html` — simple login form posting to `/login`, but backend currently has no login endpoint in this repo.
- `frontend/converter.html` — contains a file upload form, source/target selectors, and a mock submit handler that only shows an alert.
- `frontend/schema_generator.html` — contains a client-side schema generator and download flow, with no backend integration.

Backend integration requirements
- `POST /convert` — multipart file upload with `file` form field. Optional form fields: `source_db`, `target_db`.
- `POST /convert_text` — JSON payload: `{ sql_text, source_db, target_db }`.
- `GET /health` — health check.
- CORS is enabled in the backend for local origins such as `http://localhost` and `http://127.0.0.1`.

Required changes for current pages

`frontend/converter.html`
- Replace the current mock `handleSubmit()` alert behavior with a real upload to the backend.
- Use `FormData` to send `fileUpload`, `sourceDatabase`, and `targetDatabase` to `http://localhost:8000/convert`.
- Update element IDs or map existing IDs to the backend field names:
  - file input: `fileUpload`
  - source select: `sourceDatabase`
  - target select: `targetDatabase`
- Display backend response data instead of only showing the alert.

`frontend/login.html`
- Either add a backend `/login` endpoint or remove/replace the login form.
- If login is unnecessary, keep this page as a placeholder or redirect users to `converter.html`.

`frontend/schema_generator.html`
- This page currently works offline to build SQL and download a file.
- If you want backend support, add a `fetch` call to send generated SQL to `/convert_text` or another backend endpoint.
- Otherwise keep it as a self-contained schema generator.

Missing pages needing implementation
- `frontend/admin.html` — implement admin controls or remove the file if unused.
- `frontend/dashboard.html` — add dashboard content or use an existing page instead.
- `frontend/reports.html` — implement report listing or analytics.

Suggested integration for `frontend/converter.html`

Example JavaScript for backend upload:

```javascript
async function handleSubmit(event) {
  event.preventDefault();

  const file = document.getElementById('fileUpload').files[0];
  const source = document.getElementById('sourceDatabase').value;
  const target = document.getElementById('targetDatabase').value;

  if (!file || !source || !target) {
    alert('Please fill in all required fields');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);
  formData.append('source_db', source);
  formData.append('target_db', target);

  const res = await fetch('http://localhost:8000/convert', {
    method: 'POST',
    body: formData,
  });

  const data = await res.json();
  if (!res.ok) {
    alert('Conversion failed: ' + (data.detail || data.message || JSON.stringify(data)));
    return;
  }

  console.log('Conversion result:', data);
  alert('Migration completed successfully. See console for details.');
}
```

If you want, I can also update `frontend/converter.html` and `frontend/js/script.js` with a working backend integration implementation.
