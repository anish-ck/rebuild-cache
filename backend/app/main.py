import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.database import engine
from app.database.models import Base
from app.database.seed import seed_reels
from app.services.cache_service import cache_service

from app.api.profile import router as profile_router
from app.api.reels import router as reels_router
from app.api.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Run seed
    await seed_reels()
    
    # Init Redis
    await cache_service.connect()
    
    yield
    
    # Close connections
    await cache_service.close()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router, prefix="/api")
app.include_router(reels_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

app.include_router(profile_router)
app.include_router(reels_router)
app.include_router(stats_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
