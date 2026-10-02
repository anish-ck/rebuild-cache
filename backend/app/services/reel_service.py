import base64
import time
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.database.models import Reel
from app.services.cache_service import cache_service
from app.services.metrics_service import metrics_service

class ReelService:
    def _encode_cursor(self, dt: datetime, reel_id: int) -> str:
        dt_str = dt.isoformat()
        cursor_str = f"{dt_str}|{reel_id}"
        return base64.urlsafe_b64encode(cursor_str.encode()).decode('utf-8')
        
    def _decode_cursor(self, cursor: str) -> tuple[datetime, int]:
        # Handle padding if necessary
        padded_cursor = cursor + '=' * (-len(cursor) % 4)
        cursor_str = base64.urlsafe_b64decode(padded_cursor).decode('utf-8')
        dt_str, reel_id_str = cursor_str.split('|')
        return datetime.fromisoformat(dt_str), int(reel_id_str)

    async def get_reels(self, db, cursor: str | None, limit: int = 20) -> dict:
        # 1. Check cache
        cached = await cache_service.get_cached_reels(cursor, limit)
        if cached:
            return cached
            
        # 3. Cache miss, query DB
        start_time = time.perf_counter()
        
        query = select(Reel).where(Reel.creator_id == 1).order_by(Reel.created_at.desc(), Reel.id.desc()).limit(limit + 1)
        
        if cursor:
            # Decode cursor
            clean_cursor = cursor.replace('prefetch', '')
            try:
                dt, reel_id = self._decode_cursor(clean_cursor)
                query = query.where(
                    (Reel.created_at < dt) | 
                    ((Reel.created_at == dt) & (Reel.id < reel_id))
                )
            except Exception:
                pass
                
        result = await db.execute(query)
        reels = result.scalars().all()
        
        # 4. Track DB query time and event
        end_time = time.perf_counter()
        db_latency_ms = (end_time - start_time) * 1000
        await metrics_service.record_db_latency(db_latency_ms)
        await metrics_service.increment("db_queries")
        await metrics_service.add_event("DATABASE QUERY", f"Retrieved {len(reels[:limit])} reels from PostgreSQL ({db_latency_ms:.1f}ms)")
        
        # 5. Determine has_more
        has_more = len(reels) > limit
        items = reels[:limit]
        
        # 6. Build next_cursor
        next_cursor = None
        if items:
            last_item = items[-1]
            next_cursor = self._encode_cursor(last_item.created_at, last_item.id)
            
        # Format response
        response = {
            "items": [
                {
                    "id": r.id,
                    "creator_id": r.creator_id,
                    "caption": r.caption,
                    "created_at": r.created_at.isoformat(),
                    "media_key": r.media_key,
                    "thumbnail_key": r.thumbnail_key,
                    "storage_tier": r.storage_tier,
                    "view_count": r.view_count
                } for r in items
            ],
            "next_cursor": next_cursor,
            "has_more": has_more
        }
        
        # 7. Cache result
        await cache_service.cache_reels(cursor, response, limit)
        
        return response
        
    async def get_profile(self, db) -> dict:
        import json
        cache_key = "profile:1"
        if cache_service.redis:
            cached = await cache_service.redis.get(cache_key)
            if cached:
                await metrics_service.increment("redis_hits")
                await metrics_service.add_event("CACHE HIT", f"Profile loaded from Redis ({cache_key})")
                return json.loads(cached)
            else:
                await metrics_service.increment("redis_misses")

        start_time = time.perf_counter()
        result = await db.execute(select(func.count(Reel.id)).where(Reel.creator_id == 1))
        count = result.scalar()
        db_latency_ms = (time.perf_counter() - start_time) * 1000
        await metrics_service.record_db_latency(db_latency_ms)
        await metrics_service.increment("db_queries")
        await metrics_service.add_event("DATABASE QUERY", f"COUNT(*) on reels for creator_id=1 ({db_latency_ms:.1f}ms)")
        
        profile_data = {
            "username": "tech_creator",
            "total_reels": count or 0,
            "avatar_url": None
        }
        
        if cache_service.redis:
            await cache_service.redis.set(cache_key, json.dumps(profile_data), ex=300)
            await metrics_service.increment("redis_sets")
            await metrics_service.add_event("CACHE SET", f"Cached profile in Redis ({cache_key})")

        return profile_data

reel_service = ReelService()
