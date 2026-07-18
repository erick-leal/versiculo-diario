from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dates import today
from app.database import get_db
from app.models import DailyVerse, Reflection
from app.schemas import DailyVerseOut

router = APIRouter()


@router.get("/daily-verse", response_model=DailyVerseOut)
def get_daily_verse(db: Session = Depends(get_db)) -> DailyVerse:
    daily_verse = (
        db.query(DailyVerse)
        .join(Reflection, DailyVerse.reflection_id == Reflection.id)
        .filter(DailyVerse.date == today(), Reflection.status == "published")
        .first()
    )
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="No hay versículo programado para hoy")
    return daily_verse


@router.get("/daily-verse/{daily_verse_id}", response_model=DailyVerseOut)
def get_daily_verse_by_id(daily_verse_id: int, db: Session = Depends(get_db)) -> DailyVerse:
    daily_verse = (
        db.query(DailyVerse)
        .join(Reflection, DailyVerse.reflection_id == Reflection.id)
        .filter(DailyVerse.id == daily_verse_id, Reflection.status == "published")
        .first()
    )
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="Versículo no encontrado")
    return daily_verse
