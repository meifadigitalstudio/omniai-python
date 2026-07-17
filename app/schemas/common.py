from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class Meta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None


class PaginatedResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: list[T]
    meta: Meta


class ErrorResponse(BaseModel):
    success: bool
    message: str
    errors: dict | None = None


class MessageResponse(BaseModel):
    message: str