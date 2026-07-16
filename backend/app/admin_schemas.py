from datetime import datetime

from pydantic import BaseModel


class AdminVerseOut(BaseModel):
    id: int
    book: str
    chapter: int
    verse_start: int
    verse_end: int | None
    reference: str
    text: str
    translation: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VerseCreate(BaseModel):
    book: str
    chapter: int
    verse_start: int
    verse_end: int | None = None
    text: str
    translation: str = "RVA1909"


class VerseUpdate(BaseModel):
    book: str | None = None
    chapter: int | None = None
    verse_start: int | None = None
    verse_end: int | None = None
    text: str | None = None
    translation: str | None = None
