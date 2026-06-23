import redis.asyncio as aioredis
from app.config import settings


# Centralized Redis instance that can be imported anywhere
redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
