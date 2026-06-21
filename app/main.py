from fastapi import FastAPI
# from app.database import engine, Base

app = FastAPI(title="TelePulse Real-Time Logistics Telematics API")


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": "healthy", "message": "LogiStream Infrastructure Online"}
