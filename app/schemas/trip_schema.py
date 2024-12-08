from typing import List, Optional
from datetime import datetime
import strawberry

@strawberry.type
class TripResponse:
    id: int
    vendor_id: Optional[int]
    passenger_count: Optional[int]
    pickup_longitude: Optional[float]
    pickup_latitude: Optional[float]
    pickup_datetime: Optional[datetime]
    dropoff_datetime: Optional[datetime]
    trip_duration: Optional[int]

@strawberry.type
class TripsResponse:
    limit: int
    offset: int
    total_records: int
    trips: List[TripResponse]
