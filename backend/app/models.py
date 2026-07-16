import uuid
from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, ForeignKey, Text, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Verse(Base):
    __tablename__ = "verses"

    id: Mapped[int] = mapped_column(primary_key=True)
    book: Mapped[str] = mapped_column(Text)
    chapter: Mapped[int]
    verse_start: Mapped[int]
    verse_end: Mapped[int | None]
    reference: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)
    translation: Mapped[str] = mapped_column(Text, default="RVA1909")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Reflection(Base):
    __tablename__ = "reflections"

    id: Mapped[int] = mapped_column(primary_key=True)
    verse_id: Mapped[int] = mapped_column(ForeignKey("verses.id"))
    title: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="draft")
    source: Mapped[str] = mapped_column(Text, default="human")
    author_name: Mapped[str | None] = mapped_column(Text)
    reviewed_by: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    verse: Mapped["Verse"] = relationship()


class DailyVerse(Base):
    __tablename__ = "daily_verses"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, unique=True)
    verse_id: Mapped[int] = mapped_column(ForeignKey("verses.id"))
    reflection_id: Mapped[int] = mapped_column(ForeignKey("reflections.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    verse: Mapped["Verse"] = relationship()
    reflection: Mapped["Reflection"] = relationship()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str | None] = mapped_column(Text, unique=True)
    auth_provider: Mapped[str | None] = mapped_column(Text)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_seen_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "daily_verse_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    daily_verse_id: Mapped[int] = mapped_column(ForeignKey("daily_verses.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    daily_verse: Mapped["DailyVerse"] = relationship()


class AppSettings(Base):
    __tablename__ = "app_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    dark_mode: Mapped[str] = mapped_column(Text, default="system")
    # Opt-in, no opt-out: recien se activa cuando el usuario lo pide
    # explicitamente desde Configuracion (ahi se pide permiso del SO).
    notification_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_time: Mapped[time] = mapped_column(Time, default=time(8, 0))


class PushToken(Base):
    __tablename__ = "push_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    expo_push_token: Mapped[str] = mapped_column(Text, unique=True)
    platform: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_used_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class QuoteImage(Base):
    __tablename__ = "quote_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
