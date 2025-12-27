from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List, Optional

class TrackerEntryBase(BaseModel):
    mood_rating: int
    notes: Optional[str] = None
    
class TrackerEntry(TrackerEntryBase):
    id: int
    timestamp: datetime
    owner_id: int
    
    class Config:
        orm_mode = True

class TrackerSummary(BaseModel):
    average_mood: float
    total_entries: int
    best_day_entry: Optional[TrackerEntry] = None
    worst_day_entry: Optional[TrackerEntry] = None
    
    class Config:
        orm_mode = True
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class EntryCreate(BaseModel):
    mood_rating: int = Field(..., ge=1, le=5, description="Mood rating from 1 (Bad) to 5 (Great)")
    notes: Optional[str] = Field(None, description="Notes about the entry (optional)")

class EntryResponse(BaseModel):
    id: int
    mood_rating: int
    notes: Optional[str] = None
    timestamp: datetime
    owner_id: int
    
    class Config:
        orm_mode = True

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def password_must_be_different(cls, v, values):
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('New password must be different from current password.')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        return v