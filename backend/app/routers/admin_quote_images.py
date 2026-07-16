from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.admin_auth import require_admin
from app.admin_schemas import AdminQuoteImageOut, QuoteImageCreate, QuoteImageUpdate
from app.database import get_db
from app.models import QuoteImage

router = APIRouter(prefix="/admin/quote-images", dependencies=[Depends(require_admin)])


@router.get("", response_model=list[AdminQuoteImageOut])
def list_quote_images(db: Session = Depends(get_db)) -> list[QuoteImage]:
    return db.query(QuoteImage).order_by(QuoteImage.created_at.desc()).all()


@router.post("", response_model=AdminQuoteImageOut, status_code=201)
def create_quote_image(payload: QuoteImageCreate, db: Session = Depends(get_db)) -> QuoteImage:
    image = QuoteImage(image_url=payload.image_url)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.put("/{image_id}", response_model=AdminQuoteImageOut)
def update_quote_image(
    image_id: int, payload: QuoteImageUpdate, db: Session = Depends(get_db)
) -> QuoteImage:
    image = db.query(QuoteImage).filter(QuoteImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="No encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(image, field, value)

    db.commit()
    db.refresh(image)
    return image


@router.delete("/{image_id}", status_code=204)
def delete_quote_image(image_id: int, db: Session = Depends(get_db)) -> None:
    image = db.query(QuoteImage).filter(QuoteImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(image)
    db.commit()
