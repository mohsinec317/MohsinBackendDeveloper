from sqlalchemy import Column, Integer, String, DateTime, Float, Numeric
from app.models.database_model import Base

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer)
    passenger_count = Column(Integer)
    pickup_longitude = Column(Numeric(precision=10, scale=6))
    pickup_latitude = Column(Numeric(precision=10, scale=6)) 
    pickup_datetime = Column(DateTime)
    dropoff_datetime = Column(DateTime)
    trip_duration = Column(Integer)

