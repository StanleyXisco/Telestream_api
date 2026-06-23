import asyncio
import random
import time
from datetime import datetime, timezone
import httpx

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
FLEET_SIZE = 5         # Number of vehicles to simulate concurrently
PING_INTERVAL = 2      # Seconds to wait between GPS pings per vehicle
TOTAL_PINGS = 10       # How many times each vehicle will report its location


async def register_vehicle(client: httpx.AsyncClient, vehicle_id: str, driver_name: str):
    """Ensures the vehicle is registered in the database before streaming."""
    url = f"{API_BASE_URL}/vehicles"
    payload = {
        "id": vehicle_id,
        "driver_name": driver_name,
        "status": "active"
    }
    try:
        response = await client.post(url, json=payload)
        if response.status_code == 201:
            print(print(f"✅ Registered: {vehicle_id} (Driver: {driver_name})"))
        elif response.status_code == 400:
            print(f"ℹ️ {vehicle_id} already registered. Skipping creation.")
    except Exception as e:
        print(f"❌ Failed to connect to API during registration for {vehicle_id}: {e}")


async def simulate_vehicle_trip(client: httpx.AsyncClient, vehicle_id: str):
    """Simulates a vehicle driving by incrementally moving its GPS coordinates."""
    url = f"{API_BASE_URL}/telemetry"

    # Starting coordinates (centered roughly around San Francisco)
    lon = -122.4194 + random.uniform(-0.01, 0.01)
    lat = 37.7749 + random.uniform(-0.01, 0.01)
    speed = 50  # Starting speed in km/h

    print(f"🚀 Starting stream for {vehicle_id}...")

    for i in range(TOTAL_PINGS):
        # Micro-adjust position to simulate motion
        lon += random.uniform(-0.0005, 0.0005)
        lat += random.uniform(-0.0005, 0.0005)
        speed = max(0, speed + random.randint(-5, 5))  # Dynamic speed shifts

        payload = {
            "vehicle_id": vehicle_id,
            "longitude": round(lon, 6),
            "latitude": round(lat, 6),
            "speed": speed,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        try:
            start_time = time.time()
            response = await client.post(url, json=payload)
            latency = (time.time() - start_time) * 1000

            if response.status_code == 202:
                print(f"🛰️ [{vehicle_id}] Ping {i+1}/{TOTAL_PINGS} | Lat: {payload['latitude']}, Lon: {payload['longitude']} | Speed: {speed}km/h | Latency: {latency:.1f}ms")
            else:
                print(f"⚠️ [{vehicle_id}] Unexpected response {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ [{vehicle_id}] Connection error: {e}")

        await asyncio.sleep(PING_INTERVAL)

    print(f"🏁 Finished stream for {vehicle_id}.")


async def main():
    # Dynamic list of drivers
    drivers = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George"]

    # Limits connection pools to simulate real-world clients cleanly
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)

    # FIX: Combined the initialization and async context manager cleanly into one line
    async with httpx.AsyncClient(limits=limits, timeout=5.0) as client:
        print("--- PHASE 1: INITIALIZING FLEET REGISTRATION ---")
        registration_tasks = []
        for i in range(1, FLEET_SIZE + 1):
            v_id = f"vehicle_{100 + i}"
            d_name = drivers[(i - 1) % len(drivers)]
            registration_tasks.append(register_vehicle(client, v_id, d_name))

        await asyncio.gather(*registration_tasks)

        print("\n--- PHASE 2: COMMENCING CONCURRENT TELEMETRY STREAM ---")
        trip_tasks = []
        for i in range(1, FLEET_SIZE + 1):
            v_id = f"vehicle_{100 + i}"
            trip_tasks.append(simulate_vehicle_trip(client, v_id))

        await asyncio.gather(*trip_tasks)

if __name__ == "__main__":
    asyncio.run(main())
