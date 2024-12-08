import strawberry
from typing import List
from sqlalchemy.orm import Session
from app.models.trip_model import Trip
from app.schemas.trip_schema import TripResponse, TripsResponse

@strawberry.type
class Query:
    @strawberry.field
    def get_trips(self, info, limit: int = 10, offset: int = 0) -> TripsResponse:
        session: Session = info.context["session"]
        total_trips = session.query(Trip).count()
        trips = session.query(Trip).offset(offset).limit(limit).all()
        trip_list = [
            TripResponse(
                id=index+1,
                vendor_id=trip.vendor_id,
                passenger_count=trip.passenger_count,
                pickup_longitude=trip.pickup_longitude,
                pickup_latitude=trip.pickup_latitude,
                pickup_datetime=trip.pickup_datetime,
                dropoff_datetime=trip.dropoff_datetime,
                trip_duration=trip.trip_duration
            )
            for index, trip in enumerate(trips)
        ]

        return TripsResponse(
            limit=limit,
            offset=offset,
            total_records=total_trips,
            trips=trip_list
        )
