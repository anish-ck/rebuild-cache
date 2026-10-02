export interface Reel {
  id: number;
  creator_id: number;
  caption: string;
  created_at: string;
  media_key: string;
  thumbnail_key: string;
  storage_tier: string;
  view_count: number;
}

export interface ReelListResponse {
  items: Reel[];
  next_cursor: string | null;
  has_more: boolean;
}

export interface Stats {
  redis_hits: number;
  redis_misses: number;
  redis_sets: number;
  db_queries: number;
  avg_db_latency_ms: number;
  client_cache_hits: number;
  client_cache_misses: number;
  evictions: number;
  cold_storage_requests: number;
  warm_storage_requests: number;
  hot_storage_requests: number;
  prefetch_requests: number;
}

export interface SystemEvent {
  timestamp: string;
  event_type: string;
  details: string;
}
