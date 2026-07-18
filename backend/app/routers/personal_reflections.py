from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_or_create_user
from app.models import DailyVerse, PersonalReflection, User
from app.schemas import PersonalReflectionOut, PersonalReflectionUpsert

router = APIRouter()


@router.get("/personal-reflections", response_model=list[PersonalReflectionOut])
def list_personal_reflections(
    user: User = Depends(get_or_create_user), db: Session = Depends(get_db)
) -> list[PersonalReflection]:
    return (
        db.query(PersonalReflection)
        .filter(PersonalReflection.user_id == user.id)
        .order_by(PersonalReflection.updated_at.desc())
        .all()
    )


@router.put("/personal-reflections", response_model=PersonalReflectionOut)
def upsert_personal_reflection(
    payload: PersonalReflectionUpsert,
    user: User = Depends(get_or_create_user),
    db: Session = Depends(get_db),
) -> PersonalReflection:
    daily_verse = db.query(DailyVerse).filter(DailyVerse.id == payload.daily_verse_id).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="daily_verse_id no existe")

    entry = (
        db.query(PersonalReflection)
        .filter(
            PersonalReflection.user_id == user.id,
            PersonalReflection.daily_verse_id == payload.daily_verse_id,
        )
        .first()
    )
    if entry is None:
        entry = PersonalReflection(
            user_id=user.id, daily_verse_id=payload.daily_verse_id, body=payload.body
        )
        db.add(entry)
    else:
        entry.body = payload.body
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/personal-reflections/{personal_reflection_id}", status_code=204)
def delete_personal_reflection(
    personal_reflection_id: int,
    user: User = Depends(get_or_create_user),
    db: Session = Depends(get_db),
) -> None:
    entry = (
        db.query(PersonalReflection)
        .filter(
            PersonalReflection.id == personal_reflection_id,
            PersonalReflection.user_id == user.id,
        )
        .first()
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Reflexion personal no encontrada")
    db.delete(entry)
    db.commit()
