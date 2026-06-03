# backend/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from converter import convert_sql
from validator import validate_sql
from report_generator import generate_report


app = FastAPI(title="SQL Migrator")

# Allow cross-origin requests from typical local frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000", "http://127.0.0.1", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files at /static (optional)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def home():
    return {
        "message": "Welcome to SQL Migrator API"
    }


@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    source_db: str = "mysql",
    target_db: str = "postgresql"
):
    try:
        # Read uploaded SQL file
        content = await file.read()
        sql_text = content.decode("utf-8")

        # Convert SQL
        converted_sql = convert_sql(
            sql_text,
            source_db,
            target_db
        )

        # Validate converted SQL
        validation_result = validate_sql(converted_sql)

        # Generate migration report
        report = generate_report(
            source_db,
            target_db,
            validation_result
        )

        # Ensure validation_result is serializable
        validation_serializable = (
            validation_result.to_dict()
            if hasattr(validation_result, "to_dict")
            else validation_result
        )

        return JSONResponse(
            content={
                "status": "success",
                "source_database": source_db,
                "target_database": target_db,
                "converted_sql": converted_sql,
                "validation": validation_serializable,
                "report": report,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {
        "status": "running"
    }


@app.post("/convert_text")
def convert_text(payload: dict):
    """Convert SQL provided in JSON body: { sql_text, source_db, target_db }"""
    sql_text = payload.get("sql_text")
    source_db = payload.get("source_db", "mysql")
    target_db = payload.get("target_db", "postgresql")

    if not sql_text:
        raise HTTPException(status_code=400, detail="Missing 'sql_text' in request body")

    try:
        converted_sql = convert_sql(sql_text, source_db, target_db)
        validation_result = validate_sql(converted_sql)
        report = generate_report(source_db, target_db, validation_result)

        validation_serializable = (
            validation_result.to_dict()
            if hasattr(validation_result, "to_dict")
            else validation_result
        )

        return {
            "status": "success",
            "converted_sql": converted_sql,
            "validation": validation_serializable,
            "report": report,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
