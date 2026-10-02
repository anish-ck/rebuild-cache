import asyncio
from datetime import datetime
from collections import deque

class MetricsService:
    def __init__(self):
        self.lock = asyncio.Lock()
        
        self.redis_hits = 0
        self.redis_misses = 0
        self.redis_sets = 0
        self.db_queries = 0
        self.cold_storage_requests = 0
        self.warm_storage_requests = 0
        self.hot_storage_requests = 0
        self.prefetch_requests = 0
        
        self.client_cache_hits = 0
        self.client_cache_misses = 0
        self.evictions = 0
        
        self.db_latencies = []
        self.events = deque(maxlen=50)

    async def increment(self, counter_name: str):
        async with self.lock:
            if hasattr(self, counter_name):
                val = getattr(self, counter_name)
                setattr(self, counter_name, val + 1)

    async def record_client_stats(self, hits: int, misses: int, evictions: int):
        async with self.lock:
            self.client_cache_hits = hits
            self.client_cache_misses = misses
            self.evictions = evictions

    async def record_db_latency(self, ms: float):
        async with self.lock:
            self.db_latencies.append(ms)

    async def add_event(self, event_type: str, details: str):
        async with self.lock:
            self.events.append({
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "details": details
            })

    async def get_stats(self) -> dict:
        async with self.lock:
            avg_db_latency = 0.0
            if self.db_latencies:
                avg_db_latency = sum(self.db_latencies) / len(self.db_latencies)
                
            return {
                "redis_hits": self.redis_hits,
                "redis_misses": self.redis_misses,
                "redis_sets": self.redis_sets,
                "db_queries": self.db_queries,
                "avg_db_latency_ms": round(avg_db_latency, 2),
                "client_cache_hits": self.client_cache_hits,
                "client_cache_misses": self.client_cache_misses,
                "evictions": self.evictions,
                "cold_storage_requests": self.cold_storage_requests,
                "warm_storage_requests": self.warm_storage_requests,
                "hot_storage_requests": self.hot_storage_requests,
                "prefetch_requests": self.prefetch_requests,
            }

    async def get_events(self) -> list:
        async with self.lock:
            return list(self.events)

    async def reset(self):
        async with self.lock:
            self.redis_hits = 0
            self.redis_misses = 0
            self.redis_sets = 0
            self.db_queries = 0
            self.cold_storage_requests = 0
            self.warm_storage_requests = 0
            self.hot_storage_requests = 0
            self.prefetch_requests = 0
            self.client_cache_hits = 0
            self.client_cache_misses = 0
            self.evictions = 0
            self.db_latencies.clear()
            self.events.clear()

metrics_service = MetricsService()
