from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_or_create_user
from app.models import AppSettings, User
from app.schemas import AppSettingsOut, AppSettingsUpdate

router = APIRouter()


def _get_or_create_settings(user: User, db: Session) -> AppSettings:
    settings = db.query(AppSettings).filter(AppSettings.user_id == user.id).first()
    if settings is None:
        settings = AppSettings(user_id=user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.get("/settings", response_model=AppSettingsOut)
def get_settings(
    user: User = Depends(get_or_create_user), db: Session = Depends(get_db)
) -> AppSettings:
    return _get_or_create_settings(user, db)


@router.put("/settings", response_model=AppSettingsOut)
def update_settings(
    payload: AppSettingsUpdate,
    user: User = Depends(get_or_create_user),
    db: Session = Depends(get_db),
) -> AppSettings:
    settings = _get_or_create_settings(user, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return settings
