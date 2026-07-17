from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.responses import success_response
from app.modules.auth.dependencies import get_db
from app.modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
    RegisterRequest,
    UserResponse,
)
from app.modules.auth.schemas.auth import OTPResendRequest, OTPVerifyRequest
from app.modules.auth.services import AuthService
from user_agents import parse

from app.modules.auth.services.auth_service import HTTPData

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/register",
    status_code=201,
)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    data = await auth_service.register(request)
    return success_response(
        data=data,
        message="User registered successfully",
    )

@router.post(
    "/register/verify-otp"
)
async def verify_registration(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    message = await auth_service.registration_verify(request)
    return success_response(
        data=None,
        message=message,
    )

@router.post(
    "/register/resend-otp"
)
async def resend_registration_otp(request: OTPResendRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    message = await auth_service.registration_resend_otp(request)
    return success_response(
        data=None,
        message=message,
    )

@router.post(
    "/login"
)
def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)

    ip_address = (
        http_request.headers.get("X-Forwarded-For")
        or http_request.client.host
    )
    user_agent = http_request.headers.get("User-Agent")
    ua = parse(user_agent)
    device_info = (
        f"{ua.os.family} | "
        f"{ua.browser.family} | "
        f"{ua.device.family}"
    )

    http_data = HTTPData(
        ip_address=ip_address,
        user_agent=user_agent,
        device_info=device_info,
    )

    data = auth_service.login(http_data, request)


    return success_response(
        data=data,
        message="Login successful",
    )
