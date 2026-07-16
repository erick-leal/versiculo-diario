from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.admin_auth import require_admin
from app.admin_schemas import AdminReflectionOut, ReflectionCreate, ReflectionUpdate
from app.database import get_db
from app.models import Reflection, Verse

router = APIRouter(prefix="/admin/reflections", dependencies=[Depends(require_admin)])

REVIEWED_STATUSES = {"reviewed", "published"}


@router.get("", response_model=list[AdminReflectionOut])
def list_reflections(db: Session = Depends(get_db)) -> list[Reflection]:
    return db.query(Reflection).order_by(Reflection.created_at.desc()).limit(200).all()


@router.post("", response_model=AdminReflectionOut, status_code=201)
def create_reflection(
    payload: ReflectionCreate,
    claims: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Reflection:
    verse = db.query(Verse).filter(Verse.id == payload.verse_id).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="verse_id no existe")

    data = payload.model_dump()
    reviewed_by = claims.get("email") if payload.status in REVIEWED_STATUSES else None
    reflection = Reflection(**data, reviewed_by=reviewed_by)
    db.add(reflection)
    db.commit()
    db.refresh(reflection)
    return reflection


@router.put("/{reflection_id}", response_model=AdminReflectionOut)
def update_reflection(
    reflection_id: int,
    payload: ReflectionUpdate,
    claims: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Reflection:
    reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
    if reflection is None:
        raise HTTPException(status_code=404, detail="Reflexión no encontrada")

    if payload.verse_id is not None:
        verse = db.query(Verse).filter(Verse.id == payload.verse_id).first()
        if verse is None:
            raise HTTPException(status_code=404, detail="verse_id no existe")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(reflection, field, value)

    if "status" in updates and updates["status"] in REVIEWED_STATUSES:
        reflection.reviewed_by = claims.get("email")

    db.commit()
    db.refresh(reflection)
    return reflection


@router.delete("/{reflection_id}", status_code=204)
def delete_reflection(reflection_id: int, db: Session = Depends(get_db)) -> None:
    reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
    if reflection is None:
        raise HTTPException(status_code=404, detail="Reflexión no encontrada")

    db.delete(reflection)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede borrar: la reflexión está programada en el calendario",
        )
