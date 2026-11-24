from fastapi import HTTPException
from sqlalchemy.orm import Query, Session

from app.core.dates import today
from app.models import DailyVerse, Reflection


def visible_daily_verses(db: Session) -> Query:
    """Punto de partida OBLIGATORIO de toda consulta PUBLICA de dias.

    Visible = reflexion publicada (revision humana) Y fecha <= hoy. Lo segundo
    importa porque el cron auto-schedule-verse publica con 3 dias de colchon:
    sin ese filtro, pidiendo /daily-verse/{id} con el id siguiente se leia el
    contenido de manana. Los endpoints admin_* NO usan esto (el admin si
    necesita ver el futuro).
    """
    return (
        db.query(DailyVerse)
        .join(Reflection, DailyVerse.reflection_id == Reflection.id)
        .filter(Reflection.status == "published", DailyVerse.date <= today())
    )


def visible_daily_verse_ids(db: Session):
    """Subconsulta de ids visibles, para filtrar listados (favoritos, diario)."""
    return visible_daily_verses(db).with_entities(DailyVerse.id)


def get_visible_daily_verse_or_404(db: Session, daily_verse_id: int, detail: str) -> DailyVerse:
    daily_verse = visible_daily_verses(db).filter(DailyVerse.id == daily_verse_id).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail=detail)
    return daily_verse
