from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# --- TELEMETRY INGESTION SCHEMAS ---
class TelemetryCreate(BaseModel):
    vehicle_id: str = Field(..., example="vehicle_101")
    longitude: float = Field(..., ge=-180, le=180, example=-122.4194)
    latitude: float = Field(..., ge=-90, le=90, example=37.7749)
    speed: Optional[int] = Field(None, ge=0, description="Speed in km/h", example=65)
    timestamp: Optional[datetime] = None


class TelemetryResponse(BaseModel):
    id: int
    vehicle_id: str
    longitude: float
    latitude: float
    speed: Optional[int]
    timestamp: datetime

    class Config:
        from_attributes = True


# --- VEHICLE MANAGEMENT SCHEMAS ---
class VehicleCreate(BaseModel):
    id: str = Field(..., example="vehicle_101")
    driver_name: str = Field(..., example="Stanley")
    status: Optional[str] = Field("active", example="active")


class VehicleResponse(BaseModel):
    id: str
    driver_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
