from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.constants import MOOD_TAGS
from app.core.dates import today
from app.database import get_db
from app.models import DailyVerse, Reflection
from app.queries import get_visible_daily_verse_or_404, visible_daily_verses
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
    # visible = publicado Y fecha <= hoy: el cron publica con dias de
    # anticipacion y antes se podia leer el contenido de manana por id.
    return get_visible_daily_verse_or_404(db, daily_verse_id, "Versículo no encontrado")


@router.get("/reflections/by-mood", response_model=DailyVerseOut)
def get_reflection_by_mood(
    mood: str, exclude_id: int | None = None, db: Session = Depends(get_db)
) -> DailyVerse:
    if mood not in MOOD_TAGS:
        raise HTTPException(status_code=400, detail="Estado de ánimo inválido")

    # Antes el azar podia elegir un dia futuro ya programado por el cron.
    query = visible_daily_verses(db).filter(Reflection.mood_tags.any(mood))

    daily_verse = None
    if exclude_id is not None:
        daily_verse = query.filter(DailyVerse.id != exclude_id).order_by(func.random()).first()
    if daily_verse is None:
        daily_verse = query.order_by(func.random()).first()

    if daily_verse is None:
        raise HTTPException(
            status_code=404, detail="No hay reflexiones publicadas para ese estado de ánimo"
        )
    return daily_verse
