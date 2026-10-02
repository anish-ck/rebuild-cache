import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.database.database import async_session
from app.database.models import Reel

async def seed_reels():
    async with async_session() as session:
        # Check if we already have data
        result = await session.execute(select(func.count(Reel.id)))
        count = result.scalar()
        if count and count > 0:
            print("Data already exists, skipping seed.")
            return

        print("Seeding 10,000 reels...")
        batch_size = 1000
        reels = []
        now = datetime.now()
        
        # We want ID 10000 to be the most recent, ID 1 to be the oldest (one year ago)
        # So created_at increases as id increases
        for i in range(1, 10001):
            days_ago = 365 - (i * 365 / 10000.0)
            created_at = now - timedelta(days=days_ago)
            
            # cyclic keys
            cycle_idx = (i % 10) + 1
            
            # tier logic
            if i > 8000:
                tier = 'hot'
            elif i > 4000:
                tier = 'warm'
            else:
                tier = 'cold'
                
            reels.append(Reel(
                id=i,
                creator_id=1,
                caption=f"Amazing reel #{i} 🎬 #viral #trending",
                created_at=created_at,
                media_key=f"media/sample_{cycle_idx}.mp4",
                thumbnail_key=f"thumbnails/thumb_{cycle_idx}.jpg",
                storage_tier=tier,
                view_count=random.randint(100, 1000000)
            ))
            
            if len(reels) >= batch_size:
                session.add_all(reels)
                await session.commit()
                reels = []

        if reels:
            session.add_all(reels)
            await session.commit()
            
        print("Seeding complete.")
