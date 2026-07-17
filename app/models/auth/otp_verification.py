from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, DateTime, Boolean, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel

class OTPPurpose(str, Enum):
    REGISTER = "REGISTER"
    LOGIN = "LOGIN"
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
    CHANGE_EMAIL = "CHANGE_EMAIL"

class OTPVerification(BaseModel):
    __tablename__ = "otp_verifications"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    otp_hash: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    attempt: Mapped[int] = mapped_column(nullable=False, default=0)
    purpose: Mapped[OTPPurpose] = mapped_column(SQLEnum(OTPPurpose), nullable=False)