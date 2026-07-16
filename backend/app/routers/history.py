from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DailyVerse, Reflection
from app.schemas import DailyVerseOut

router = APIRouter()


@router.get("/history", response_model=list[DailyVerseOut])
def list_history(db: Session = Depends(get_db)) -> list[DailyVerse]:
    today = datetime.now(timezone.utc).date()
    return (
        db.query(DailyVerse)
        .join(Reflection, DailyVerse.reflection_id == Reflection.id)
        .filter(DailyVerse.date <= today, Reflection.status == "published")
        .order_by(DailyVerse.date.desc())
        .limit(30)
        .all()
    )
