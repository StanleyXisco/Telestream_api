from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Vehicle, LocationLog
from app.schemas import TelemetryCreate
from app.redis_client import redis_client

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def ingest_telemetry(payload: TelemetryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.id == payload.vehicle_id))
    vehicle = result.scalar_one_or_none()

    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle {payload.vehicle_id} not found")

    spatial_point = f"POINT({payload.longitude} {payload.latitude})"
    timestamp_to_use = payload.timestamp if payload.timestamp else datetime.now(timezone.utc)

    # 1. Historical logging inside PostgreSQL
    new_log = LocationLog(
        vehicle_id=payload.vehicle_id,
        coordinates=spatial_point,
        speed=payload.speed,
        timestamp=timestamp_to_use
    )
    db.add(new_log)

    # 2. Fast caching inside Redis
    redis_key = f"vehicle:{payload.vehicle_id}:latest"
    await redis_client.hset(redis_key, mapping={
        "longitude": str(payload.longitude),
        "latitude": str(payload.latitude),
        "speed": str(payload.speed or 0),
        "timestamp": timestamp_to_use.isoformat()
    })

    await db.commit()
    return {"status": "queued", "message": "Telemetry data processed successfully"}
