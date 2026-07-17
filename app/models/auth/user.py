from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(150))

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(255),
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
