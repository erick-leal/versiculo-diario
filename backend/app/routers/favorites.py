from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_or_create_user
from app.models import DailyVerse, Favorite, User
from app.schemas import FavoriteCreate, FavoriteOut

router = APIRouter()


@router.get("/favorites", response_model=list[FavoriteOut])
def list_favorites(
    user: User = Depends(get_or_create_user), db: Session = Depends(get_db)
) -> list[Favorite]:
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )


@router.post("/favorites", response_model=FavoriteOut, status_code=201)
def add_favorite(
    payload: FavoriteCreate,
    user: User = Depends(get_or_create_user),
    db: Session = Depends(get_db),
) -> Favorite:
    daily_verse = db.query(DailyVerse).filter(DailyVerse.id == payload.daily_verse_id).first()
    if daily_verse is None:
        raise HTTPException(status_code=404, detail="daily_verse_id no existe")

    existing = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id, Favorite.daily_verse_id == payload.daily_verse_id)
        .first()
    )
    if existing is not None:
        return existing

    favorite = Favorite(user_id=user.id, daily_verse_id=payload.daily_verse_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


@router.delete("/favorites/{favorite_id}", status_code=204)
def remove_favorite(
    favorite_id: int,
    user: User = Depends(get_or_create_user),
    db: Session = Depends(get_db),
) -> None:
    favorite = (
        db.query(Favorite)
        .filter(Favorite.id == favorite_id, Favorite.user_id == user.id)
        .first()
    )
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    db.delete(favorite)
    db.commit()
