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


class PersonalReflectionOut(BaseModel):
    id: int
    daily_verse_id: int
    body: str
    created_at: datetime
    updated_at: datetime
    daily_verse: DailyVerseOut

    model_config = {"from_attributes": True}


class PersonalReflectionUpsert(BaseModel):
    daily_verse_id: int
    body: str


class AppSettingsOut(BaseModel):
    dark_mode: Literal["light", "dark", "system"]
    morning_reminder_enabled: bool
    morning_reminder_time: time
    night_reminder_enabled: bool
    night_reminder_time: time

    model_config = {"from_attributes": True}


class AppSettingsUpdate(BaseModel):
    dark_mode: Literal["light", "dark", "system"] | None = None
    morning_reminder_enabled: bool | None = None
    morning_reminder_time: time | None = None
    night_reminder_enabled: bool | None = None
    night_reminder_time: time | None = None
