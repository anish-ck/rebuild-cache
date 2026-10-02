from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.reel_service import reel_service
from app.schemas.reel import ProfileResponse

router = APIRouter()

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(db: AsyncSession = Depends(get_db)):
    return await reel_service.get_profile(db)
