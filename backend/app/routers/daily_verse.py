from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DailyVerse
from app.schemas import DailyVerseOut

router = APIRouter()


@router.get("/daily-verse", response_model=DailyVerseOut)
def get_daily_verse(db: Session = Depends(get_db)) -> DailyVerse:
    # "Hoy" se define en UTC, no en la zona horaria implicita del proceso.
    # Revisar si conviene un corte por zona horaria de usuario queda para
    # cuando la app tenga configuracion de usuario real (ver app_settings.timezone).
    today = datetime.now(timezone.utc).date()
    daily_verse = db.query(DailyVerse).filter(DailyVerse.date == today).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="No hay versículo programado para hoy")
    return daily_verse
