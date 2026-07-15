from datetime import date

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
    date: date
    verse: VerseOut
    reflection: ReflectionOut
