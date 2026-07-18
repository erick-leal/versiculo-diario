from datetime import date as date_type
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

from app.constants import MOOD_TAGS

ReflectionStatus = Literal["draft", "ai_generated", "reviewed", "published"]
ReflectionSource = Literal["human", "ai_assisted"]


def _validate_mood_tags(value: list[str]) -> list[str]:
    invalid = set(value) - set(MOOD_TAGS)
    if invalid:
        raise ValueError(f"mood_tags inválidos: {sorted(invalid)}")
    return value


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


class AdminReflectionOut(BaseModel):
    id: int
    verse_id: int
    verse: AdminVerseOut
    title: str | None
    body: str
    status: ReflectionStatus
    source: ReflectionSource
    author_name: str | None
    reviewed_by: str | None
    mood_tags: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReflectionCreate(BaseModel):
    verse_id: int
    title: str | None = None
    body: str
    status: ReflectionStatus = "draft"
    source: ReflectionSource = "human"
    author_name: str | None = None
    mood_tags: list[str] = []

    @field_validator("mood_tags")
    @classmethod
    def _check_mood_tags(cls, value: list[str]) -> list[str]:
        return _validate_mood_tags(value)


class ReflectionUpdate(BaseModel):
    verse_id: int | None = None
    title: str | None = None
    body: str | None = None
    status: ReflectionStatus | None = None
    source: ReflectionSource | None = None
    author_name: str | None = None
    mood_tags: list[str] | None = None

    @field_validator("mood_tags")
    @classmethod
    def _check_mood_tags(cls, value: list[str] | None) -> list[str] | None:
        return None if value is None else _validate_mood_tags(value)


class AdminDailyVerseOut(BaseModel):
    id: int
    date: date_type
    verse_id: int
    reflection_id: int
    verse: AdminVerseOut
    reflection: AdminReflectionOut

    model_config = {"from_attributes": True}


class DailyVerseCreate(BaseModel):
    date: date_type
    verse_id: int
    reflection_id: int


class DailyVerseUpdate(BaseModel):
    date: date_type | None = None
    verse_id: int | None = None
    reflection_id: int | None = None


class AdminQuoteImageOut(BaseModel):
    id: int
    image_url: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class QuoteImageCreate(BaseModel):
    image_url: str


class QuoteImageUpdate(BaseModel):
    is_active: bool | None = None
