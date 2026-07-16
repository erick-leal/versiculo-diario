from datetime import date, datetime

from pydantic import BaseModel


class VerseOut(BaseModel):
    reference: str
    text: str
    translation: str

    model_config = {"from_attributes": True}


class ReflectionOut(BaseModel):
    title: str | None
    body: str
    author_name: str | None

    model_config = {"from_attributes": True}


class DailyVerseOut(BaseModel):
    id: int
    date: date
    verse: VerseOut
    reflection: ReflectionOut

    model_config = {"from_attributes": True}


class FavoriteOut(BaseModel):
    id: int
    created_at: datetime
    daily_verse: DailyVerseOut

    model_config = {"from_attributes": True}


class FavoriteCreate(BaseModel):
    daily_verse_id: int
