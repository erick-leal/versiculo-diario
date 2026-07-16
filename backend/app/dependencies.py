import uuid
from datetime import datetime, timezone

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


def get_or_create_user(x_device_id: str = Header(...), db: Session = Depends(get_db)) -> User:
    try:
        device_uuid = uuid.UUID(x_device_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="X-Device-Id invalido")

    user = db.query(User).filter(User.id == device_uuid).first()
    if user is None:
        user = User(id=device_uuid)
        db.add(user)
    else:
        user.last_seen_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user
