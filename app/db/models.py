from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now())

    chat_messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="user",
        cascade="save-update, delete, delete-orphan, merge, expunge")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now())

    user: Mapped["User"] = relationship(back_populates="chat_messages")
