from pathlib import Path
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class EmailSchema(BaseModel):
    to: list[EmailStr]
    subject: str
    template_name: str
    context: dict[str, Any] = Field(default_factory=dict)
    attachments: list[Path] | None = None