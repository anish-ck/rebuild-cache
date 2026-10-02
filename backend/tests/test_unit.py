import pytest
from datetime import datetime
from app.services.reel_service import reel_service
from app.services.storage_service import storage_service
from app.services.metrics_service import MetricsService
from app.schemas.reel import ReelSchema, StatsResponse, ProfileResponse

def test_cursor_encoding_and_decoding():
    dt = datetime(2026, 5, 20, 14, 30, 45, 123456)
    reel_id = 8520
    
    encoded = reel_service._encode_cursor(dt, reel_id)
    assert isinstance(encoded, str)
    assert len(encoded) > 0
    
    decoded_dt, decoded_id = reel_service._decode_cursor(encoded)
    assert decoded_dt == dt
    assert decoded_id == reel_id

def test_storage_tier_calculation():
    # Latest 2000 reels: HOT (id > 8000)
    assert storage_service.get_tier(8001) == "hot"
    assert storage_service.get_tier(10000) == "hot"
    
    # Middle 4000: WARM (4001 to 8000)
    assert storage_service.get_tier(8000) == "warm"
    assert storage_service.get_tier(4001) == "warm"
    
    # Oldest 4000: COLD (1 to 4000)
    assert storage_service.get_tier(4000) == "cold"
    assert storage_service.get_tier(1) == "cold"

def test_storage_latencies():
    assert storage_service.get_latency("hot") == 20
    assert storage_service.get_latency("HOT") == 20
    assert storage_service.get_latency("warm") == 100
    assert storage_service.get_latency("cold") == 500

@pytest.mark.asyncio
async def test_metrics_service_counters_and_events():
    ms = MetricsService()
    
    await ms.increment("redis_hits")
    await ms.increment("redis_hits")
    await ms.increment("redis_misses")
    await ms.record_db_latency(12.5)
    await ms.record_db_latency(17.5)
    await ms.add_event("CACHE HIT", "Key: reels:first_page")
    await ms.record_client_stats(hits=10, misses=2, evictions=1)
    
    stats = await ms.get_stats()
    assert stats["redis_hits"] == 2
    assert stats["redis_misses"] == 1
    assert stats["avg_db_latency_ms"] == 15.0
    assert stats["client_cache_hits"] == 10
    assert stats["client_cache_misses"] == 2
    assert stats["evictions"] == 1
    
    events = await ms.get_events()
    assert len(events) == 1
    assert events[0]["event_type"] == "CACHE HIT"
    
    await ms.reset()
    reset_stats = await ms.get_stats()
    assert reset_stats["redis_hits"] == 0
    assert reset_stats["db_queries"] == 0
    assert len(await ms.get_events()) == 0

def test_pydantic_schemas():
    now = datetime.now()
    reel_data = {
        "id": 1,
        "creator_id": 1,
        "caption": "Test reel",
        "created_at": now,
        "media_key": "media/sample_1.mp4",
        "thumbnail_key": "thumbnails/thumb_1.jpg",
        "storage_tier": "cold",
        "view_count": 50000
    }
    reel = ReelSchema(**reel_data)
    assert reel.id == 1
    assert reel.storage_tier == "cold"
    
    stats_data = {
        "redis_hits": 10,
        "redis_misses": 5,
        "redis_sets": 8,
        "db_queries": 6,
        "avg_db_latency_ms": 14.2,
        "client_cache_hits": 20,
        "client_cache_misses": 3,
        "evictions": 1,
        "cold_storage_requests": 2,
        "warm_storage_requests": 4,
        "hot_storage_requests": 15,
        "prefetch_requests": 3
    }
    stats = StatsResponse(**stats_data)
    assert stats.redis_hits == 10
    assert stats.avg_db_latency_ms == 14.2

