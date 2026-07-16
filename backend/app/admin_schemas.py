from datetime import date as date_type
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

ReflectionStatus = Literal["draft", "ai_generated", "reviewed", "published"]
ReflectionSource = Literal["human", "ai_assisted"]


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


class ReflectionUpdate(BaseModel):
    verse_id: int | None = None
    title: str | None = None
    body: str | None = None
    status: ReflectionStatus | None = None
    source: ReflectionSource | None = None
    author_name: str | None = None


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
