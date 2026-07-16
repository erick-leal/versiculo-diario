from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.admin_auth import require_admin
from app.admin_schemas import AdminDailyVerseOut, DailyVerseCreate, DailyVerseUpdate
from app.database import get_db
from app.models import DailyVerse, Reflection, Verse

router = APIRouter(prefix="/admin/daily-verses", dependencies=[Depends(require_admin)])


def _validate_pair(db: Session, verse_id: int, reflection_id: int) -> None:
    verse = db.query(Verse).filter(Verse.id == verse_id).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="verse_id no existe")

    reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
    if reflection is None:
        raise HTTPException(status_code=404, detail="reflection_id no existe")

    if reflection.verse_id != verse_id:
        raise HTTPException(
            status_code=400, detail="La reflexión elegida no corresponde a ese versículo"
        )


@router.get("", response_model=list[AdminDailyVerseOut])
def list_daily_verses(db: Session = Depends(get_db)) -> list[DailyVerse]:
    return db.query(DailyVerse).order_by(DailyVerse.date.desc()).limit(200).all()


@router.post("", response_model=AdminDailyVerseOut, status_code=201)
def create_daily_verse(payload: DailyVerseCreate, db: Session = Depends(get_db)) -> DailyVerse:
    _validate_pair(db, payload.verse_id, payload.reflection_id)

    daily_verse = DailyVerse(**payload.model_dump())
    db.add(daily_verse)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Ya hay un versículo programado para esa fecha"
        )
    db.refresh(daily_verse)
    return daily_verse


@router.put("/{daily_verse_id}", response_model=AdminDailyVerseOut)
def update_daily_verse(
    daily_verse_id: int, payload: DailyVerseUpdate, db: Session = Depends(get_db)
) -> DailyVerse:
    daily_verse = db.query(DailyVerse).filter(DailyVerse.id == daily_verse_id).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="No encontrado")

    updates = payload.model_dump(exclude_unset=True)
    verse_id = updates.get("verse_id", daily_verse.verse_id)
    reflection_id = updates.get("reflection_id", daily_verse.reflection_id)
    if "verse_id" in updates or "reflection_id" in updates:
        _validate_pair(db, verse_id, reflection_id)

    for field, value in updates.items():
        setattr(daily_verse, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Ya hay un versículo programado para esa fecha"
        )
    db.refresh(daily_verse)
    return daily_verse


@router.delete("/{daily_verse_id}", status_code=204)
def delete_daily_verse(daily_verse_id: int, db: Session = Depends(get_db)) -> None:
    daily_verse = db.query(DailyVerse).filter(DailyVerse.id == daily_verse_id).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="No encontrado")

    db.delete(daily_verse)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede borrar: hay favoritos de usuarios que apuntan a esta fecha",
        )
