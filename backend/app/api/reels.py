from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.database.database import get_db
from app.database.models import Reel
from app.services.reel_service import reel_service
from app.services.storage_service import storage_service
from app.services.metrics_service import metrics_service
from app.schemas.reel import ReelListResponse

router = APIRouter()

@router.get("/reels")
async def get_reels(limit: int = 20, cursor: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if cursor and 'prefetch' in cursor:
        await metrics_service.increment("prefetch_requests")
        
    return await reel_service.get_reels(db, cursor, limit)

@router.get("/reels/{reel_id}/media")
async def get_media(reel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reel).where(Reel.id == reel_id))
    reel = result.scalar_one_or_none()
    
    if not reel:
        raise HTTPException(status_code=404, detail="Reel not found")
        
    media_info = await storage_service.get_media(reel)
    
    # If cold, promote to hot
    if media_info["tier"].lower() == "cold":
        await storage_service.promote(reel_id, db)
        
    return media_info
