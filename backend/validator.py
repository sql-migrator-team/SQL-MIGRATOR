# validator.py

import re
from typing import Dict, List, Tuple


class ValidationResult:
    def __init__(self):
        self.valid = True
        self.errors = []
        self.warnings = []

    def add_error(self, message):
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    def to_dict(self):
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings
        }


class SQLValidator:

    MYSQL_TYPES = {
        "INT",
        "INTEGER",
        "BIGINT",
        "SMALLINT",
        "TINYINT",
        "VARCHAR",
        "TEXT",
        "LONGTEXT",
        "MEDIUMTEXT",
        "DATETIME",
        "TIMESTAMP",
        "DATE",
        "FLOAT",
        "DOUBLE",
        "DECIMAL",
        "BOOLEAN",
        "CHAR",
        "BLOB",
        "JSON"
    }

    POSTGRES_TYPES = {
        "INTEGER",
        "BIGINT",
        "SMALLINT",
        "VARCHAR",
        "TEXT",
        "TIMESTAMP",
        "DATE",
        "REAL",
        "DOUBLE PRECISION",
        "NUMERIC",
        "BOOLEAN",
        "CHAR",
        "BYTEA",
        "JSON",
        "JSONB"
    }

    UNSUPPORTED_KEYWORDS = [
        "ENGINE=",
        "AUTO_INCREMENT",
        "UNSIGNED",
        "ZEROFILL",
        "ENUM(",
        "SET(",
        "LOCK TABLES",
        "UNLOCK TABLES"
    ]

    def validate_sql(self, sql_text: str) -> ValidationResult:

        result = ValidationResult()

        if not sql_text:
            result.add_error("SQL content is empty.")
            return result

        self._validate_create_table(sql_text, result)
        self._validate_datatypes(sql_text, result)
        self._validate_mysql_features(sql_text, result)
        self._validate_foreign_keys(sql_text, result)

        return result

    def _validate_create_table(
        self,
        sql_text: str,
        result: ValidationResult
    ):

        create_tables = re.findall(
            r'CREATE\s+TABLE',
            sql_text,
            re.IGNORECASE
        )

        if not create_tables:
            result.add_warning(
                "No CREATE TABLE statements found."
            )

    def _validate_datatypes(
        self,
        sql_text: str,
        result: ValidationResult
    ):

        datatype_pattern = re.findall(
            r'\b([A-Z]+)\s*(?:\(|,|\s)',
            sql_text.upper()
        )

        ignore_keywords = {
            "CREATE",
            "TABLE",
            "PRIMARY",
            "KEY",
            "FOREIGN",
            "REFERENCES",
            "NOT",
            "NULL",
            "DEFAULT",
            "UNIQUE",
            "CONSTRAINT"
        }

        for datatype in datatype_pattern:

            if datatype in ignore_keywords:
                continue

            if datatype in self.MYSQL_TYPES:
                continue

            if datatype in self.POSTGRES_TYPES:
                continue

    def _validate_mysql_features(
        self,
        sql_text: str,
        result: ValidationResult
    ):

        sql_upper = sql_text.upper()

        for keyword in self.UNSUPPORTED_KEYWORDS:

            if keyword.upper() in sql_upper:

                result.add_warning(
                    f"MySQL specific feature detected: {keyword}"
                )

    def _validate_foreign_keys(
        self,
        sql_text: str,
        result: ValidationResult
    ):

        fk_matches = re.findall(
            r'FOREIGN\s+KEY\s*\((.*?)\)\s*REFERENCES\s*(.*?)\(',
            sql_text,
            re.IGNORECASE
        )

        for column, table in fk_matches:

            if not column.strip():
                result.add_error(
                    "Foreign key column missing."
                )

            if not table.strip():
                result.add_error(
                    "Referenced table missing."
                )

    def validate_connection_config(
        self,
        config: Dict
    ) -> ValidationResult:

        result = ValidationResult()

        required_fields = [
            "host",
            "port",
            "username",
            "database"
        ]

        for field in required_fields:

            if field not in config:
                result.add_error(
                    f"Missing connection field: {field}"
                )

        return result

    def validate_table_structure(
        self,
        table_schema: Dict
    ) -> ValidationResult:

        result = ValidationResult()

        if "table_name" not in table_schema:
            result.add_error(
                "Table name missing."
            )

        if "columns" not in table_schema:
            result.add_error(
                "Columns definition missing."
            )
            return result

        columns = table_schema["columns"]

        if len(columns) == 0:
            result.add_error(
                "Table contains no columns."
            )

        for column in columns:

            if "name" not in column:
                result.add_error(
                    "Column name missing."
                )

            if "type" not in column:
                result.add_error(
                    f"Datatype missing for column "
                    f"{column.get('name', 'UNKNOWN')}"
                )

        return result

    def validate_query(
        self,
        query: str
    ) -> ValidationResult:

        result = ValidationResult()

        if not query.strip():
            result.add_error(
                "Query is empty."
            )
            return result

        dangerous_patterns = [
            r"DROP\s+DATABASE",
            r"TRUNCATE\s+TABLE"
        ]

        for pattern in dangerous_patterns:

            if re.search(
                pattern,
                query,
                re.IGNORECASE
            ):
                result.add_warning(
                    f"Potentially dangerous query detected: {pattern}"
                )

        return result


def validate_sql(sql_text: str) -> ValidationResult:
    """Convenience wrapper used by the FastAPI app.

    Returns a `ValidationResult` instance.
    """
    validator = SQLValidator()
    return validator.validate_sql(sql_text)
