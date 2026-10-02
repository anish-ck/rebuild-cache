import asyncio
from sqlalchemy import update
from app.database.models import Reel
from app.services.metrics_service import metrics_service

class StorageService:
    def get_tier(self, reel_id: int) -> str:
        if reel_id > 8000:
            return 'hot'
        elif reel_id > 4000:
            return 'warm'
        return 'cold'

    def get_latency(self, tier: str) -> int:
        tier_lower = (tier or 'cold').lower()
        if tier_lower == 'hot':
            return 20
        elif tier_lower == 'warm':
            return 100
        return 500

    async def get_media(self, reel) -> dict:
        tier = (reel.storage_tier or self.get_tier(reel.id)).lower()
        latency_ms = self.get_latency(tier)
        
        await metrics_service.increment(f"{tier}_storage_requests")
        
        # Simulate storage latency
        await asyncio.sleep(latency_ms / 1000.0)
        
        event_name = "COLD STORAGE ACCESS" if tier == "cold" else f"{tier.upper()} STORAGE ACCESS"
        await metrics_service.add_event(event_name, f"Reel #{reel.id} accessed from {tier.upper()} tier ({latency_ms}ms)")
        
        return {
            "reel_id": reel.id,
            "media_key": reel.media_key,
            "tier": tier.lower(),
            "latency_ms": latency_ms
        }

    async def promote(self, reel_id: int, db):
        await db.execute(
            update(Reel).where(Reel.id == reel_id).values(storage_tier='hot')
        )
        await db.commit()
        await metrics_service.add_event("PROMOTED TO HOT", f"Reel #{reel_id} promoted to HOT cache")

storage_service = StorageService()
