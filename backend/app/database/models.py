from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Reel(Base):
    __tablename__ = "reels"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    creator_id = Column(Integer, nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    media_key = Column(Text, nullable=True)
    thumbnail_key = Column(Text, nullable=True)
    storage_tier = Column(String(10), nullable=True)
    view_count = Column(Integer, default=0)

    __table_args__ = (
        Index("idx_creator_reels", "creator_id", created_at.desc(), id.desc()),
    )
