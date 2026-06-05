# SQL Migrator Backend

SQL Migrator is a backend-only ETL system for SQL-to-SQL migration, file imports, exports, schema generation, validation, reporting, and migration history tracking.

This repository contains only the backend implementation. No HTML, CSS, JavaScript, or frontend UI is included. All frontend values are represented by placeholders in examples and request payloads.

## Project Overview

The backend system exposes REST APIs for:
- User registration, login, and role-based authentication
- SQL-to-SQL database migration
- CSV and Excel file import into SQL
- SQL table export to CSV or Excel
- Schema generation from files
- Migration validation
- Migration history and reporting
- Admin user and statistics management

The application uses SQLite for internal storage and supports external source and target databases through placeholder credentials.

## Architecture

This project follows clean architecture guidelines:
- `backend/app.py` initializes Flask and registers API routes
- `backend/config.py` handles environment and database configuration
- `backend/extensions.py` centralizes shared Flask extensions
- `backend/auth/` contains authentication logic
- `backend/converters/` handles SQL conversion and file import/export
- `backend/validators/` checks migration and compatibility results
- `backend/processors/` processes CSV/Excel files and generates table schemas
- `backend/reports/` builds JSON, text, and PDF reports
- `backend/database/` contains external database connection helpers
- `backend/models/` defines SQLAlchemy ORM models for internal storage
- `backend/routes/` defines REST API endpoints
- `backend/utils/` contains reusable utilities and helpers

## Features

- Authentication with JWT and role-based access control
- User and admin APIs
- SQL-to-SQL migration engine with datatype mapping
- CSV and Excel import into target databases
- SQL table export to CSV or Excel
- Schema generation from files
- Migration history persistence
- Text, JSON, and PDF report generation
- Secure password hashing and input sanitization
- Internal SQLite storage for users, migrations, history, and reports

## Technology Stack

- Python 3.12+
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- SQLAlchemy
- Bcrypt
- Pandas
- OpenPyXL
- python-dotenv
- pymysql
- psycopg2-binary
- cx_Oracle (optional / requires Oracle client)
- fpdf
- pytest

## Project Structure

```
SQL_migrator/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── extensions.py
│   ├── auth/
│   ├── converters/
│   ├── validators/
│   ├── processors/
│   ├── reports/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── logs/
│   ├── uploads/
│   ├── exports/
│   └── tests/
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── SYSTEM_DESIGN.md
│   └── DATABASE_SCHEMA.md
├── README.md
├── .env.example
├── requirements.txt
└── .gitignore
```

## System Requirements

- Python 3.12 or newer
- Git (recommended)
- SQLite support (bundled with Python)
- Oracle Instant Client if using `cx_Oracle`

### Supported database drivers

- `pymysql` for MySQL
- `psycopg2-binary` for PostgreSQL
- `sqlite3` for SQLite
- `cx_Oracle` for Oracle (requires separate Oracle client installation)

## Installation Guide

1. Clone or download the repository into a local directory.

2. Create a Python virtual environment:

```bash
cd '/home/ark/Downloads/new sql/SQL_migrator'
python3 -m venv .venv
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Copy the example environment file and update values as needed:

```bash
cp .env.example .env
```

6. Start the application:

```bash
python -m backend.app
```

## How to Run the Project

Use these commands from the project root:

```bash
source .venv/bin/activate
python backend/app.py
```

The backend will start on port `5000` by default.

## API Documentation

See `docs/API_DOCUMENTATION.md` for detailed endpoint descriptions, request bodies, placeholder values, example responses, and error responses.

## Placeholder Documentation

This project uses placeholder values for frontend-provided data. Common placeholders include:

| Placeholder | Purpose | Example |
|-------------|---------|---------|
| `<FRONTEND_SOURCE_DB_TYPE>` | Source database type | mysql |
| `<FRONTEND_SOURCE_HOST>` | Source database host | localhost |
| `<FRONTEND_SOURCE_PORT>` | Source database port | 3306 |
| `<FRONTEND_SOURCE_USERNAME>` | Source database username | root |
| `<FRONTEND_SOURCE_PASSWORD>` | Source database password | password123 |
| `<FRONTEND_SOURCE_DATABASE>` | Source database name | sales_db |
| `<FRONTEND_TARGET_DB_TYPE>` | Target database type | postgresql |
| `<FRONTEND_TARGET_HOST>` | Target database host | localhost |
| `<FRONTEND_TARGET_PORT>` | Target database port | 5432 |
| `<FRONTEND_TARGET_USERNAME>` | Target database username | postgres |
| `<FRONTEND_TARGET_PASSWORD>` | Target database password | password123 |
| `<FRONTEND_TARGET_DATABASE>` | Target database name | warehouse_db |
| `<FRONTEND_TABLE_NAME>` | Destination table name | migrated_users |
| `<FRONTEND_EXPORT_PATH>` | Export file path | exports/users.csv |
| `<FRONTEND_FILE_PATH>` | Upload file path | uploads/data.xlsx |
| `<FRONTEND_SECRET_KEY>` | Flask secret key | change-me |
| `<FRONTEND_JWT_SECRET_KEY>` | JWT secret key | change-me-jwt |

## Database Configuration Guide

The backend uses internal SQLite storage for users, migrations, history, and reports. External source and target database credentials are received via API request payloads.

To connect external databases, a frontend must send JSON payloads that include:

- `source_db_type` or `target_db_type`
- `host`
- `port`
- `username`
- `password`
- `database`

Supported external database engines:
- MySQL
- PostgreSQL
- SQLite
- Oracle (basic support)

Example external connection payload:

```json
{
  "source_db_type": "mysql",
  "source_host": "localhost",
  "source_port": "3306",
  "source_username": "<FRONTEND_SOURCE_USERNAME>",
  "source_password": "<FRONTEND_SOURCE_PASSWORD>",
  "source_database": "<FRONTEND_SOURCE_DATABASE>"
}
```

## Testing Guide

Run tests using pytest:

```bash
source .venv/bin/activate
python -m pytest backend/tests
```

The backend test suite verifies authentication, schema generation, and file import components.

## Future Improvements

- Add asynchronous job processing for large migrations
- Add task queue support with Celery or RQ
- Implement full schema diff and incremental migration
- Add complete Oracle production support with client installation guidance
- Add UI or Postman collection for frontend integration
- Add advanced validation rules and checksum comparison

## Troubleshooting

- `OperationalError: unable to open database file` — ensure the SQLite path exists and the application has write permission.
- `ModuleNotFoundError: config` — run the application from the project root or activate the virtual environment.
- `cx_Oracle` install failures — install Oracle Instant Client or remove Oracle support from local environment if not required.

---

## Notes

- This backend is intentionally backend-only and uses placeholders for frontend inputs.
- No HTML, CSS, or JavaScript frontend files are included.
- The internal storage is SQLite, and the external database engines are configured via request payloads.
