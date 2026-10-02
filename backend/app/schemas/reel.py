from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ReelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    caption: Optional[str] = None
    created_at: datetime
    media_key: Optional[str] = None
    thumbnail_key: Optional[str] = None
    storage_tier: Optional[str] = None
    view_count: int = 0

class ReelListResponse(BaseModel):
    items: List[ReelSchema]
    next_cursor: Optional[str] = None
    has_more: bool

class ProfileResponse(BaseModel):
    username: str
    total_reels: int
    avatar_url: Optional[str] = None

class StatsResponse(BaseModel):
    redis_hits: int
    redis_misses: int
    redis_sets: int
    db_queries: int
    avg_db_latency_ms: float
    client_cache_hits: int = 0
    client_cache_misses: int = 0
    evictions: int = 0
    cold_storage_requests: int
    warm_storage_requests: int
    hot_storage_requests: int
    prefetch_requests: int

class EventSchema(BaseModel):
    timestamp: str
    event_type: str
    details: str
