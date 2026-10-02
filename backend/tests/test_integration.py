import pytest

pytestmark = pytest.mark.asyncio

async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200

async def test_get_profile(client):
    response = await client.get("/api/profile")
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "total_reels" in data

async def test_get_reels_first_page(client):
    # Ensure fresh state
    await client.post("/api/reset")
    response = await client.get("/api/reels?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 20
    assert "next_cursor" in data
    assert "has_more" in data
    assert data["has_more"] is True

async def test_get_reels_with_cursor(client):
    response1 = await client.get("/api/reels?limit=20")
    data1 = response1.json()
    cursor = data1["next_cursor"]
    
    response2 = await client.get(f"/api/reels?cursor={cursor}&limit=20")
    data2 = response2.json()
    
    assert response2.status_code == 200
    assert len(data2["items"]) > 0
    assert data1["items"][0]["id"] != data2["items"][0]["id"]

async def test_cursor_pagination_no_overlap(client):
    res1 = await client.get("/api/reels?limit=20")
    items1 = res1.json()["items"]
    cursor = res1.json()["next_cursor"]
    
    res2 = await client.get(f"/api/reels?cursor={cursor}&limit=20")
    items2 = res2.json()["items"]
    
    ids1 = {item["id"] for item in items1}
    ids2 = {item["id"] for item in items2}
    
    assert len(ids1.intersection(ids2)) == 0

async def test_reels_limit_parameter(client):
    response = await client.get("/api/reels?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5


async def test_get_stats(client):
    response = await client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "redis_hits" in data
    assert "redis_misses" in data
    assert "db_queries" in data
    assert "cold_storage_requests" in data

async def test_reset(client):
    response = await client.post("/api/reset")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "reset"

async def test_redis_caching(client):
    await client.post("/api/reset")
    
    # First request - cache miss
    await client.get("/api/reels?limit=10")
    stats1 = (await client.get("/api/stats")).json()
    misses1 = stats1.get("redis_misses", 0)
    
    # Second request with identical params - cache hit!
    await client.get("/api/reels?limit=10")
    stats2 = (await client.get("/api/stats")).json()
    hits2 = stats2.get("redis_hits", 0)
    
    assert hits2 > 0

async def test_storage_tier_assignment(client):
    response = await client.get("/api/reels?limit=20")
    assert response.status_code == 200
    data = response.json()
    
    for item in data["items"]:
        reel_id = item["id"]
        tier = item.get("storage_tier", "").lower()
        
        if reel_id > 8000:
            assert tier == "hot"
        elif reel_id > 4000:
            assert tier == "warm"
        else:
            assert tier == "cold"

async def test_database_query_only_on_cache_miss(client):
    await client.post("/api/reset")
    
    # 1. First call - DB queried
    res1 = await client.get("/api/reels?limit=15")
    assert res1.status_code == 200
    stats1 = (await client.get("/api/stats")).json()
    db_queries_1 = stats1["db_queries"]
    assert db_queries_1 > 0
    
    # 2. Second identical call - served from Redis, DB queries count unchanged
    res2 = await client.get("/api/reels?limit=15")
    assert res2.status_code == 200
    stats2 = (await client.get("/api/stats")).json()
    db_queries_2 = stats2["db_queries"]
    assert db_queries_2 == db_queries_1
    assert stats2["redis_hits"] > stats1["redis_hits"]

async def test_cold_storage_simulation_and_promotion(client):
    await client.post("/api/reset")
    
    # Access reel #100 (which belongs to cold tier: 1..4000)
    res = await client.get("/api/reels/100/media")
    assert res.status_code == 200
    data = res.json()
    assert data["reel_id"] == 100
    assert data["latency_ms"] == 500
    
    stats = (await client.get("/api/stats")).json()
    assert stats["cold_storage_requests"] >= 1
    
    # Second access: should now be promoted to hot (20ms latency)
    res2 = await client.get("/api/reels/100/media")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["tier"] == "hot"
    assert data2["latency_ms"] == 20


