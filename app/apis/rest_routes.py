from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database_model import get_db_session
from app.models.trip_model import Trip

rest_router = APIRouter()

def validate_limit_offset(limit: int, offset: int, total_records: int):
    if limit > 500:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 0,
                "error": {
                    "message": "Limit cannot exceed 500 records"
                }
            }
        )
    if offset > total_records:
        max_offset = max(0, total_records - limit)
        raise HTTPException(
            status_code=400,
            detail={
                "status": 0,
                "error": {
                    "message": (
                        f"Offset exceeds the maximum data size. "
                        f"Total records: {total_records}. "
                        f"For the provided limit of {limit}, the maximum allowed offset is {max_offset}."
                    )
                }
            }
        )

@rest_router.get("/trips/")
def get_trips(
    limit: int = Query(..., ge=1, description="Number of records to return"),
    offset: int = Query(..., ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db_session)
):
    total_records = db.query(func.count(Trip.id)).scalar()
    validate_limit_offset(limit, offset, total_records)
    trips = db.query(Trip).limit(limit).offset(offset).all()

    if not trips:
        return {
            "status": 0,
            "error": {
                "message": "No trips found"
            }
        }

    trips_data = [
        {
            "id": index+1,
            "vendor_id": trip.vendor_id,
            "passenger_count": trip.passenger_count,
            "pickup_longitude": trip.pickup_longitude,
            "pickup_latitude": trip.pickup_latitude,
            "pickup_datetime": trip.pickup_datetime,
            "dropoff_datetime": trip.dropoff_datetime,
            "trip_duration": trip.trip_duration
        }
        for index, trip in enumerate(trips)
    ]

    return {
        "status": 1,
        "trips": trips_data,
        "limit": limit,
        "offset": offset,
        "total_records": total_records
    }


@rest_router.post("/trips/summary")
async def get_trips_summary(
    request: Request,
    db: Session = Depends(get_db_session)
):
    data = await request.json()
    summary_type = data.get("type")
    limit = data.get("limit", 10)

    if summary_type == "date_summary":
        return get_date_summary(db)
    elif summary_type == "avg_duration":
        return get_avg_duration(db)
    elif summary_type == "passenger_count_summary":
        return get_passenger_count_summary(db)
    elif summary_type == "vendor_summary":
        return get_vendor_summary(db)
    elif summary_type == "longest_trip":
        return get_longest_trip(db)
    elif summary_type == "shortest_trip":
        return get_shortest_trip(db)
    elif summary_type == "pickup_location_summary":
        return get_pickup_location_summary(db)
    elif summary_type == "trip_duration_distribution":
        return get_trip_duration_distribution(db)
    elif summary_type == "trip_count_per_month":
        return get_trip_count_per_month(db)
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid summary type"
        )

def get_date_summary(db: Session):
    total_trips_per_day = db.query(
        func.date(Trip.pickup_datetime).label('trip_date'),
        func.count(Trip.id).label('total_trips')
    ).group_by(func.date(Trip.pickup_datetime)).all()

    return {
        "status": 1,
        "summary": {
            "total_trips_per_day": [
                {"date": str(trip_date), "total_trips": total_trips}
                for trip_date, total_trips in total_trips_per_day
            ]
        }
    }

def get_avg_duration(db: Session):
    avg_trip_duration = db.query(func.avg(Trip.trip_duration)).scalar()
    return {
        "status": 1,
        "summary": {"average_trip_duration": avg_trip_duration}
    }

def get_passenger_count_summary(db: Session):
    passenger_count_per_day = db.query(
        func.date(Trip.pickup_datetime).label('trip_date'),
        func.sum(Trip.passenger_count).label('total_passengers')
    ).group_by(func.date(Trip.pickup_datetime)).all()

    return {
        "status": 1,
        "summary": {
            "total_passenger_count_per_day": [
                {"date": str(trip_date), "total_passengers": total_passengers}
                for trip_date, total_passengers in passenger_count_per_day
            ]
        }
    }

def get_vendor_summary(db: Session):
    vendor_summary = db.query(
        Trip.vendor_id,
        func.count(Trip.id).label('total_trips')
    ).group_by(Trip.vendor_id).all()

    return {
        "status": 1,
        "summary": {
            "vendor_summary": [
                {"vendor_id": vendor_id, "total_trips": total_trips}
                for vendor_id, total_trips in vendor_summary
            ]
        }
    }

def get_longest_trip(db: Session):
    longest_trip = db.query(
        Trip.id,
        Trip.trip_duration,
        Trip.pickup_datetime,
        Trip.dropoff_datetime
    ).order_by(Trip.trip_duration.desc()).first()

    return {
        "status": 1,
        "summary": {
            "longest_trip": {
                "id": longest_trip.id,
                "duration": longest_trip.trip_duration,
                "pickup_datetime": longest_trip.pickup_datetime,
                "dropoff_datetime": longest_trip.dropoff_datetime
            }
        }
    }

def get_shortest_trip(db: Session):
    shortest_trip = db.query(
        Trip.id,
        Trip.trip_duration,
        Trip.pickup_datetime,
        Trip.dropoff_datetime
    ).order_by(Trip.trip_duration.asc()).first()

    return {
        "status": 1,
        "summary": {
            "shortest_trip": {
                "id": shortest_trip.id,
                "duration": shortest_trip.trip_duration,
                "pickup_datetime": shortest_trip.pickup_datetime,
                "dropoff_datetime": shortest_trip.dropoff_datetime
            }
        }
    }

def get_pickup_location_summary(db: Session, limit: int = 100):
    pickup_location_summary = db.query(
        Trip.pickup_latitude,
        Trip.pickup_longitude,
        func.count(Trip.id).label('total_trips')
    ).group_by(Trip.pickup_latitude, Trip.pickup_longitude).limit(limit).all()

    return {
        "status": 1,
        "summary": {
            "pickup_location_summary": [
                {"latitude": lat, "longitude": long, "total_trips": total_trips}
                for lat, long, total_trips in pickup_location_summary
            ]
        }
    }

def get_trip_duration_distribution(db: Session):
    duration_buckets = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400]
    distribution = {}
    for bucket_start in duration_buckets:
        bucket_end = bucket_start + 300
        count = db.query(func.count(Trip.id)).filter(
            Trip.trip_duration >= bucket_start,
            Trip.trip_duration < bucket_end
        ).scalar()
        distribution[f"{bucket_start}-{bucket_end}"] = count

    return {
        "status": 1,
        "summary": {"trip_duration_distribution": distribution}
    }

def get_trip_count_per_month(db: Session):
    trip_count_per_month = db.query(
        func.to_char(Trip.pickup_datetime, "YYYY-MM").label("month"),  # Use TO_CHAR for PostgreSQL
        func.count(Trip.id).label("total_trips")
    ).group_by(func.to_char(Trip.pickup_datetime, "YYYY-MM")).all()

    return {
        "status": 1,
        "summary": {
            "trip_count_per_month": [
                {"month": month, "total_trips": total_trips}
                for month, total_trips in trip_count_per_month
            ]
        }
    }