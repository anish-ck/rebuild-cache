import os
import json
from redis.asyncio import Redis
from app.services.metrics_service import metrics_service

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

class CacheService:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = Redis.from_url(REDIS_URL, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    def _get_key(self, cursor: str | None, limit: int = 20) -> str:
        if not cursor:
            return "reels:first_page" if limit == 20 else f"reels:first_page:{limit}"
        return f"reels:cursor:{cursor}" if limit == 20 else f"reels:cursor:{cursor}:{limit}"

    async def get_cached_reels(self, cursor: str | None, limit: int = 20) -> dict | None:
        if not self.redis:
            return None
            
        key = self._get_key(cursor, limit)
        data = await self.redis.get(key)
        
        if data:
            await metrics_service.increment("redis_hits")
            await metrics_service.add_event("CACHE HIT", f"Key: {key}")
            return json.loads(data)
        else:
            await metrics_service.increment("redis_misses")
            return None

    async def cache_reels(self, cursor: str | None, data: dict, limit: int = 20, ttl: int = 300):
        if not self.redis:
            return
            
        key = self._get_key(cursor, limit)
        await self.redis.set(key, json.dumps(data), ex=ttl)
        await metrics_service.increment("redis_sets")
        await metrics_service.add_event("CACHE SET", f"Key: {key}, TTL: {ttl}s")

    async def invalidate_all(self):
        if self.redis:
            await self.redis.flushall()
            await metrics_service.add_event("CACHE_INVALIDATE", "All keys flushed")

cache_service = CacheService()
