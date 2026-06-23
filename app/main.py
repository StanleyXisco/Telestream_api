from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.vehicles import router as vehicles_router
from app.api.v1.telemetry import router as telemetry_router
# from app.database import engine, Base

app = FastAPI(title="TelePulse Real-Time Logistics Telematics API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(vehicles_router, prefix="/api/v1")
app.include_router(telemetry_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "healthy", "message": "LogiStream Infrastructure Online"}
