from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship 
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    entries = relationship("TrackerEntry", back_populates="owner")


class TrackerEntry(Base):
    __tablename__ = "tracker_entries"

    id = Column(Integer, primary_key=True, index=True)
    mood_rating = Column(Integer, nullable=False) 
    notes = Column(Text, nullable=True) 
    timestamp = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id")) 
    owner = relationship("User", back_populates="entries")