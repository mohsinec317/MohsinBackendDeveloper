from pydantic import BaseModel

class CsvPathRequest(BaseModel):
    csv_path: str