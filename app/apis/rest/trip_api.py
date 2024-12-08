from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db_session
from app.models.trip_model import Trip
from sqlalchemy import select
from app.schemas.trip_schema import TripResponse

rest_router = APIRouter()

@rest_router.get("/trips/", response_model=List[TripResponse])
def get_trips(limit: int = 10, offset: int = 0, db: Session = Depends(get_db_session)):

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100 records")
    
    statement = select(Trip).limit(limit).offset(offset)
    print("Statement")
    print(statement)
    trips = db.query(Trip).offset(offset).limit(limit).all()
    print("trips:")
    print(trips)
    
    if not trips:
        raise HTTPException(status_code=404, detail="No trips found")
    
    return {"trips": trips}

