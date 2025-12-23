from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models 
from .. import schemas
from app.database import get_db
from app.auth import get_current_username 

router = APIRouter(prefix="/tracker", tags=["Tracker"])

def get_user_id(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

@router.post("/", response_model=schemas.EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(
    entry: schemas.EntryCreate, 
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_username) 
):
    owner_id = get_user_id(db, current_username)
    
    db_entry = models.TrackerEntry(
        mood_rating=entry.mood_rating,
        notes=entry.notes,
        owner_id=owner_id
    )

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/", response_model=list[schemas.EntryResponse])
def read_entries(
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_username),
    skip: int = 0, 
    limit: int = 100
):
    owner_id = get_user_id(db, current_username)
    
    entries = (
        db.query(models.TrackerEntry)
        .filter(models.TrackerEntry.owner_id == owner_id)
        .order_by(models.TrackerEntry.timestamp.desc()) 
        .offset(skip)
        .limit(limit)
        .all()
    )
    return entries

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_username),
):
    owner_id = get_user_id(db, current_username)
    
    average_mood = (
        db.query(func.avg(models.TrackerEntry.mood_rating))
        .filter(models.TrackerEntry.owner_id == owner_id)
        .scalar()
    )

    return {
        "average_mood": round(average_mood, 2) if average_mood is not None else 0.0,
        "total_entries": db.query(models.TrackerEntry).filter(models.TrackerEntry.owner_id == owner_id).count()
    }

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_username)
):
    owner_id = get_user_id(db, current_username)
    
    entry = db.query(models.TrackerEntry).filter(
        models.TrackerEntry.id == entry_id,
        models.TrackerEntry.owner_id == owner_id
    ).first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found or you do not have permission to delete it"
        )

    db.delete(entry)
    db.commit()
    
    return {"message": "Entry deleted successfully"}