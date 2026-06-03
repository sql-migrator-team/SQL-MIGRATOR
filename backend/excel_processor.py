# excel_processor.py

import pandas as pd

class ExcelProcessor:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_schema(self):
        """
        Reads Excel schema file and returns table structure.
        Expected Columns:
        Table_Name | Column_Name | Data_Type | Constraints
        """

        try:
            df = pd.read_excel(self.file_path)

            schema = {}

            for _, row in df.iterrows():
                table = str(row["Table_Name"]).strip()

                column_info = {
                    "column_name": str(row["Column_Name"]).strip(),
                    "data_type": str(row["Data_Type"]).strip(),
                    "constraints": str(row.get("Constraints", "")).strip()
                }

                if table not in schema:
                    schema[table] = []

                schema[table].append(column_info)

            return schema

        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":

    file_path = "sample_schema.xlsx"

    processor = ExcelProcessor(file_path)

    schema = processor.read_schema()

    print(schema)
