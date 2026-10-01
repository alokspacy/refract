"""SQLAlchemy model for flashcards."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Integer
from app.db.database import Base

class FlashcardDeckModel(Base):
    __tablename__ = "flashcard_decks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    cards = Column(JSON, nullable=False, default=list)
    total_cards = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
