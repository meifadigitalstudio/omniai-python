from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.common.helpers import otp
from app.common.helpers.datetime_helper import utc_now
from app.common.helpers.otp import generate_otp
from app.core import logger
from app.common.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.auth.otp_verification import OTPPurpose, OTPVerification
from app.models.auth.refresh_token import RefreshToken
from app.models.auth.user import User

from app.modules.auth.dependencies import (
    InvalidCredentialsException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.modules.auth.repositories import (
    UserRepository,
    OTPRepository,
    RefreshRepository,
    RoleRepository,
)
from app.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)

from app.modules.auth.schemas.auth import OTPResendRequest, OTPVerifyRequest
from app.thirdparty.mail import (
    EmailSchema,
    EmailService
)


OTP_EXPIRE_MINUTES = 10

@dataclass
class HTTPData:
    ip_address: str
    user_agent: str
    device_info: str

class AuthService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.user_repository = UserRepository(db)
        self.otp_repository = OTPRepository(db)
        self.role_repository = RoleRepository(db)
        self.refresh_token_repository = RefreshRepository(db)

    async def register(self, request: RegisterRequest) -> UserResponse:
        existing_user_by_email = self.user_repository.get_by_email(request.email)
        if existing_user_by_email:
            raise EmailAlreadyExistsException("Email already exists")

        existing_user_by_username = self.user_repository.get_by_username(request.username)
        if existing_user_by_username:
            raise UsernameAlreadyExistsException("Username already exists")

        get_user_role = self.role_repository.get_by_code("USER")
        hashed_password = hash_password(request.password)

        new_user = User(
            full_name=request.full_name,
            email=request.email,
            username=request.username,
            password=hashed_password,
            role_id=get_user_role.id if get_user_role else None
        )

        otp_generate = generate_otp(6)
        expired_time = datetime.now() + timedelta(minutes=OTP_EXPIRE_MINUTES)
        otp_hash = hash_password(otp_generate)
        
        try:
            self.user_repository.create(new_user)
            self.db.flush()

            otp = OTPVerification(
                user_id=new_user.id,
                email=new_user.email,
                otp_hash=otp_hash,
                expires_at=expired_time,
                purpose=OTPPurpose.REGISTER
            )
            self.otp_repository.create(otp)

            self.db.commit()
            self.db.refresh(new_user)

        except Exception as e:
            self.db.rollback()
            logger.exception(
                "Failed to send verification email | user_id={} | email={} | error={}",
                new_user.id,
                new_user.email,
                str(e),
            )
            raise

        email = EmailSchema(
            to=[new_user.email],
            subject="Verify Your Email",
            template_name="register-otp.html",
            context={
                "title": "Verify Email",
                "year": datetime.now().year,
                "name": new_user.full_name,
                "otp": otp_generate,
                "expired": f"{OTP_EXPIRE_MINUTES} minutes",
            },
        )

        try:
            await EmailService().send(email)
        except Exception:
            logger.exception(
                "Failed to send verification email to {}",
                new_user.email,
            )

        return UserResponse.model_validate(
            new_user
        )
    
    async def registration_verify(self, request: OTPVerifyRequest) -> str:
        otp_verification = self.otp_repository.get_by_email_purpose(
            email=request.email,
            purpose=OTPPurpose.REGISTER
        )

        if not otp_verification:
            raise InvalidCredentialsException("Invalid OTP or email")

        if not verify_password(request.otp, otp_verification.otp_hash):
            raise InvalidCredentialsException("Invalid OTP")
        
        if utc_now() > otp_verification.expires_at:
            raise InvalidCredentialsException("OTP has expired")

        user = self.user_repository.get_by_email(request.email)
        if not user:
            raise InvalidCredentialsException("User not found")

        try:
            user.is_verified = True
            user.email_verified_at = datetime.now()
            self.user_repository.update(user)
            self.otp_repository.delete(otp_verification)

            self.db.commit()
            self.db.refresh(user)
        except Exception as e:
            self.db.rollback()
            logger.exception(
                "Failed to verify otp email | user_id={} | email={} | error={}",
                user.id,
                user.email,
                str(e),
            )
            raise

        return "Email verified successfully"
    
    async def registration_resend_otp(self, request: OTPResendRequest) -> str:
        user = self.user_repository.get_by_email(request.email)
        if not user:
            raise InvalidCredentialsException("User not found")

        otp_verification = self.otp_repository.get_by_email_purpose(
            email=request.email,
            purpose=OTPPurpose.REGISTER
        )

        try:
            if otp_verification:
                self.otp_repository.delete(otp_verification)

            otp_generate = generate_otp(6)
            expired_time = datetime.now() + timedelta(minutes=OTP_EXPIRE_MINUTES)
            otp_hash = hash_password(otp_generate)

            new_otp = OTPVerification(
                user_id=user.id,
                email=user.email,
                otp_hash=otp_hash,
                expires_at=expired_time,
                purpose=OTPPurpose.REGISTER
            )
            self.otp_repository.create(new_otp)

            self.db.commit()
            self.db.refresh(new_otp)
        except Exception as e:
            self.db.rollback()
            logger.exception(
                "Failed to send verification email | user_id={} | email={} | error={}",
                user.id,
                user.email,
                str(e),
            )
            raise

        email_schema = EmailSchema(
            to=[user.email],
            subject="Verify Your Email",
            template_name="register-otp.html",
            context={
                "title": "Verify Email",
                "year": datetime.now().year,
                "name": user.full_name,
                "otp": otp_generate,
                "expired": f"{OTP_EXPIRE_MINUTES} minutes",
            },
        )

        try:
            await EmailService().send(email_schema)
        except Exception:
            logger.exception(
                "Failed to send verification email to {}",
                user.email,
            )

        return "OTP resent successfully"

    def login(self, http_data: HTTPData, request: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(request.identifier) or self.user_repository.get_by_username(request.identifier)

        if not user or not verify_password(request.password, user.password):
            raise InvalidCredentialsException("Invalid credentials")
        
        if not user.is_active:
            raise InvalidCredentialsException("User is not active")
        
        if not user.is_verified:
            raise InvalidCredentialsException("User is not verified")
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        hash_refresh_token = hash_password(refresh_token.token)

        try:
            user.last_login_at = datetime.now()
            self.user_repository.update(user)

            refreshData = RefreshToken(
                user_id=user.id,
                token_hash=hash_refresh_token,
                expires_at=refresh_token.expires_at,
                ip_address=http_data.ip_address,
                user_agent=http_data.user_agent,
                device_info=http_data.device_info
            )

            self.refresh_token_repository.create(refreshData)

            self.db.commit()
            self.db.refresh(user)
        except Exception as e:
            self.db.rollback()
            logger.exception(
                "Failed to update last login | user_id={} | email={} | error={}",
                user.id,
                user.email,
                str(e),
            )
            raise

        return TokenResponse(
            access_token=access_token.token,
            refresh_token=refresh_token.token
        )
