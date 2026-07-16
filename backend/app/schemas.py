from datetime import date, datetime, time
from typing import Literal

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


class AppSettingsOut(BaseModel):
    dark_mode: Literal["light", "dark", "system"]
    notification_enabled: bool
    notification_time: time

    model_config = {"from_attributes": True}


class AppSettingsUpdate(BaseModel):
    dark_mode: Literal["light", "dark", "system"] | None = None
    notification_enabled: bool | None = None
    notification_time: time | None = None
