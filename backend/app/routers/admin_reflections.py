from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.admin_auth import require_admin
from app.admin_schemas import (
    AdminReflectionOut,
    BulkPublishRequest,
    ReflectionCreate,
    ReflectionUpdate,
)
from app.database import get_db
from app.models import Reflection, Verse

router = APIRouter(prefix="/admin/reflections", dependencies=[Depends(require_admin)])

REVIEWED_STATUSES = {"reviewed", "published"}


@router.get("", response_model=list[AdminReflectionOut])
def list_reflections(db: Session = Depends(get_db)) -> list[Reflection]:
    # Límite subido de 200 a 500: con los lotes de seed_content_batch*.py el
    # total de reflexiones crece rápido y un límite bajo empieza a esconder
    # contenido viejo en este listado (aunque siga existiendo en la DB).
    return db.query(Reflection).order_by(Reflection.created_at.desc()).limit(500).all()


@router.post("/bulk-review", response_model=list[AdminReflectionOut])
def bulk_review_reflections(
    payload: BulkPublishRequest,
    claims: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[Reflection]:
    """Pasa reflexiones (típicamente 'ai_generated') a 'reviewed', sin
    publicarlas ni asignarles fecha. El cron de auto_schedule_verse las toma
    de ahí solo, día a día, y recién en ese momento las pasa a 'published'
    con una fecha asignada."""
    reflections = db.query(Reflection).filter(Reflection.id.in_(payload.ids)).all()
    missing = set(payload.ids) - {r.id for r in reflections}
    if missing:
        raise HTTPException(status_code=404, detail=f"IDs no encontrados: {sorted(missing)}")

    for reflection in reflections:
        reflection.status = "reviewed"
        reflection.reviewed_by = claims.get("email")

    db.commit()
    for reflection in reflections:
        db.refresh(reflection)
    return reflections


@router.post("/bulk-publish", response_model=list[AdminReflectionOut])
def bulk_publish_reflections(
    payload: BulkPublishRequest,
    claims: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[Reflection]:
    """Publica directamente. Pensado para reflexiones que ya tienen una
    fecha asignada a mano en el calendario (/daily-verses) y necesitan
    quedar visibles ya mismo -- NO para el lote nuevo sin fecha, que debe
    pasar por bulk-review y esperar al cron."""
    reflections = db.query(Reflection).filter(Reflection.id.in_(payload.ids)).all()
    missing = set(payload.ids) - {r.id for r in reflections}
    if missing:
        raise HTTPException(status_code=404, detail=f"IDs no encontrados: {sorted(missing)}")

    for reflection in reflections:
        reflection.status = "published"
        reflection.reviewed_by = claims.get("email")

    db.commit()
    for reflection in reflections:
        db.refresh(reflection)
    return reflections


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
