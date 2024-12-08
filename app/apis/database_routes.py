from fastapi import APIRouter, Query
from app.utilities.database_init import create_database_if_not_exists, create_table, load_csv_to_database
from app.models.database import CsvPathRequest

router = APIRouter()

@router.post("/initialize-database/")
async def initialize_database(csv_path: str = Query(...)):
    try:
        create_database_if_not_exists()
        create_table()
        load_csv_to_database(csv_path)

        return {"message": "Database initialized and data loaded successfully."}
    except Exception as e:
        return {"error": str(e)}
