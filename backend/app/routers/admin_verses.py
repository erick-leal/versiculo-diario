from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.admin_auth import require_admin
from app.admin_schemas import AdminVerseOut, VerseCreate, VerseUpdate
from app.database import get_db
from app.models import Verse
from app.utils import build_verse_reference

router = APIRouter(prefix="/admin/verses", dependencies=[Depends(require_admin)])


@router.get("", response_model=list[AdminVerseOut])
def list_verses(db: Session = Depends(get_db)) -> list[Verse]:
    return db.query(Verse).order_by(Verse.created_at.desc()).limit(200).all()


@router.post("", response_model=AdminVerseOut, status_code=201)
def create_verse(payload: VerseCreate, db: Session = Depends(get_db)) -> Verse:
    reference = build_verse_reference(
        payload.book, payload.chapter, payload.verse_start, payload.verse_end
    )
    verse = Verse(**payload.model_dump(), reference=reference)
    db.add(verse)
    db.commit()
    db.refresh(verse)
    return verse


@router.put("/{verse_id}", response_model=AdminVerseOut)
def update_verse(verse_id: int, payload: VerseUpdate, db: Session = Depends(get_db)) -> Verse:
    verse = db.query(Verse).filter(Verse.id == verse_id).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="Versículo no encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(verse, field, value)

    verse.reference = build_verse_reference(
        verse.book, verse.chapter, verse.verse_start, verse.verse_end
    )
    db.commit()
    db.refresh(verse)
    return verse


@router.delete("/{verse_id}", status_code=204)
def delete_verse(verse_id: int, db: Session = Depends(get_db)) -> None:
    verse = db.query(Verse).filter(Verse.id == verse_id).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="Versículo no encontrado")

    db.delete(verse)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede borrar: el versículo tiene reflexiones o está programado en el calendario",
        )
