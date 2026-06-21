from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, index=True) # e.g., "vehicle_101"
    driver_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LocationLog(Base):
    __tablename__ = "location_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, ForeignKey("vehicles.id"), index=True)
    
    # PostGIS Geometry column representing a point (Longitude, Latitude)
    # srid=4326 is the spatial reference system identifier for standard global GPS coordinates
    coordinates = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
