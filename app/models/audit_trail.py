
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.models import BaseModel

class AuditTrail(BaseModel):
    __tablename__ = "audit_trails"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    module: Mapped[str] = mapped_column(String(255), nullable=False)

    entity: Mapped[str] = mapped_column(String(255), nullable=True)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=True)

    ip_address: Mapped[str] = mapped_column(String(255), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)

    old_values: Mapped[str] = mapped_column(JSONB, nullable=True)
    new_values: Mapped[str] = mapped_column(JSONB, nullable=True)