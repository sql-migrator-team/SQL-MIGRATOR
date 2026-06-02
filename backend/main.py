# backend/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from converter import convert_sql
from validator import validate_sql
from report_generator import generate_report

app = FastAPI(title="SQL Migrator")


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

        return JSONResponse(
            content={
                "status": "success",
                "source_database": source_db,
                "target_database": target_db,
                "converted_sql": converted_sql,
                "validation": validation_result,
                "report": report
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


@app.get("/health")
def health_check():
    return {
        "status": "running"
    }
