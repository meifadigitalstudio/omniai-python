from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import (
    LoginRequest,
    TokenResponse,
    RegisterRequest,
    UserResponse,
)
from app.services import AuthService
from app.utils import success_response

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/register",
    status_code=201,
)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    data = auth_service.register(request)
    return success_response(
        data=data,
        message="User registered successfully",
    )

@router.post(
    "/login"
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    data = auth_service.login(request)
    return success_response(
        data=data,
        message="Login successful",
    )