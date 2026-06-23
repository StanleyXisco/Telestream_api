from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle_data: VehicleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_data.id))
    existing_vehicle = result.scalar_one_or_none()

    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle ID already registered")

    new_vehicle = Vehicle(
        id=vehicle_data.id,
        driver_name=vehicle_data.driver_name,
        status=vehicle_data.status
    )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    return new_vehicle
