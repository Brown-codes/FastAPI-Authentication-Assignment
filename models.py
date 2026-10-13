from datetime import datetime, timezone

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str | None] = mapped_column(default=None)
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
    role: Mapped[str] = mapped_column(default="user")  # "admin" | "editor" | "user"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    owner: Mapped[str] = mapped_column(ForeignKey("users.username"))
    is_public: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)