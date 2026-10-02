# 🎬 ReelCache — Where Did the Old Reels Go?

> A production-style MVP demonstrating how Instagram-like platforms efficiently retrieve thousands of reels using cursor-based pagination, caching, lazy loading, and virtualized rendering.

## 📋 Problem Statement

When a user has 10,000+ reels, how does the platform retrieve and display them efficiently? This project answers that question with a working demonstration.

## 🏗 Architecture

```
                         USER
                           |
                    Next.js Frontend
                           |
                      REST API
                           |
                    FastAPI Backend
                           |
          ┌────────────────┼────────────────┐
          |                |                |
          ▼                ▼                ▼
       Redis          PostgreSQL       Storage Layer
       Cache          Database         Simulation
                                         |
                              ┌──────────┼──────────┐
                              |          |          |
                             HOT       WARM       COLD
```

## 🛠 Tech Stack

### Frontend
- Next.js 15+ with React 19
- TypeScript
- Tailwind CSS
- TanStack Query (data fetching + caching)
- TanStack Virtual (virtualized rendering)
- Intersection Observer API

### Backend
- Python 3.12+
- FastAPI
- SQLAlchemy (async)
- Pydantic v2
- asyncpg
- redis-py

### Infrastructure
- PostgreSQL 16
- Redis 7
- Docker & Docker Compose

## 🚀 Quick Start

```bash
git clone <repo>
cd rebuild-cache
docker compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📡 API Documentation

### Profile
```
GET /api/profile
```
Returns user profile with total reel count.

### Reels Feed
```
GET /api/reels?limit=20&cursor=<cursor>
```
Returns paginated reels with cursor-based pagination.

Response:
```json
{
  "items": [{...}],
  "next_cursor": "base64_encoded_cursor",
  "has_more": true
}
```

### System Statistics
```
GET /api/stats
```
Returns cache hits/misses, DB queries, storage metrics.

### Reset
```
POST /api/reset
```
Resets all metrics and caches.

## 🔑 Key Concepts

### Cursor-Based Pagination
Cursor-based pagination is preferred over offset-based pagination as it prevents skipping or duplicating items when data changes in real-time. This project uses a compound cursor consisting of `(created_at, id)` which is base64 encoded for opaque client usage.

### Redis Caching Strategy
We use a cache-aside pattern to reduce database load. Reel queries are cached with a configured TTL. The cache key is structured to uniquely identify the pagination parameters.

### Client-Side LRU Cache
A Map-based LRU implementation on the frontend manages memory efficiently. It restricts the cache to a max of 40 pages and evicts the least recently used pages automatically.

### Virtualized Rendering
Rendering thousands of DOM elements degrades performance. Virtualization ensures that even with 500 loaded reels, only the 20-30 visible DOM elements are rendered at any time.

### Storage Tier Simulation
Reels are classified into HOT, WARM, and COLD storage tiers, simulating differences in access latency. Reels can be dynamically promoted upon access to optimize future retrievals.

### Prefetching
Predictive loading occurs 5 items before the user reaches the end of the page, providing a seamless scrolling experience without jarring pauses for loading.

## 🎯 Demo Scenarios

1. **Initial Load**: Fast fetching of the first 20 (HOT) items with instantaneous virtualized render.
2. **Infinite Scroll**: Continuous smooth scrolling as new batches of 20 items are prefetched in the background.
3. **Deep Retrieval**: Fetching COLD tier items resulting in simulated slower latency but displaying the promotion of these items to a faster tier for subsequent requests.
4. **Cache Hits**: Scrolling back up will hit the client LRU cache; revisiting recently accessed pages triggers Redis cache hits, resulting in zero DB queries.
5. **Memory Management**: When scrolling deep enough, observe the Map-based LRU evicting older pages to keep memory footprint minimal.

## 🔄 Production Mapping

| MVP Component | Production Equivalent |
|---|---|
| PostgreSQL Docker | Amazon RDS / Cloud SQL |
| Redis Docker | Amazon ElastiCache / Cloud Memorystore |
| Local Storage Sim | Amazon S3 / Cloud Storage |
| Media Cache Sim | CloudFront / Cloud CDN |
| FastAPI Docker | ECS Fargate / Cloud Run |
| Console Logs | CloudWatch / Cloud Logging |

## 📁 Project Structure

```
rebuild-cache/
├── backend/            # FastAPI application
│   ├── tests/          # Pytest suite
│   ├── app/            # Source code
│   └── Dockerfile
├── frontend/           # Next.js application
│   ├── src/            # Next.js source code
│   └── Dockerfile
├── docker-compose.yml  # Infrastructure configuration
├── .env.example        # Environment variables example
└── README.md           # This document
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# With Docker running
docker compose exec backend pytest
```

## 📊 Performance

- Expected initial load: < 100ms
- Redis cache hit latency: < 5ms
- Virtualized rendering allows maintaining a stable memory heap regardless of scroll depth.

## 📄 License
