from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DailyVerse
from app.schemas import DailyVerseOut

router = APIRouter()


@router.get("/daily-verse", response_model=DailyVerseOut)
def get_daily_verse(db: Session = Depends(get_db)) -> DailyVerse:
    daily_verse = db.query(DailyVerse).filter(DailyVerse.date == date.today()).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="No hay versículo programado para hoy")
    return daily_verse
