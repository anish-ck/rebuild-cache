from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database.database import get_db
from pydantic import BaseModel
from app.services.metrics_service import metrics_service
from app.services.cache_service import cache_service
from app.schemas.reel import StatsResponse, EventSchema
from typing import List

router = APIRouter()

class ClientStatsPayload(BaseModel):
    hits: int
    misses: int
    evictions: int

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    return await metrics_service.get_stats()

@router.post("/stats/client")
async def update_client_stats(payload: ClientStatsPayload):
    await metrics_service.record_client_stats(payload.hits, payload.misses, payload.evictions)
    return {"status": "ok"}

@router.get("/events", response_model=List[EventSchema])
async def get_events():
    return await metrics_service.get_events()

@router.post("/reset")
async def reset_stats(db: AsyncSession = Depends(get_db)):
    await metrics_service.reset()
    await cache_service.invalidate_all()
    # Reset demo state in DB (restore original tiers)
    await db.execute(
        text("""
            UPDATE reels SET storage_tier = 
                CASE 
                    WHEN id > 8000 THEN 'hot'
                    WHEN id > 4000 THEN 'warm'
                    ELSE 'cold'
                END
            WHERE (id <= 4000 AND storage_tier != 'cold')
               OR (id > 4000 AND id <= 8000 AND storage_tier != 'warm')
               OR (id > 8000 AND storage_tier != 'hot');
        """)
    )
    await db.commit()
    return {"status": "reset"}
