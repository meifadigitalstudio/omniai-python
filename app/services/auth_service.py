from sqlalchemy.orm import Session

from app.repositories import UserRepository
from app.auth import (
    InvalidCredentialsException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
    create_access_token,
    create_refresh_token
)
from app.core import (
    hash_password,
    verify_password
)
from app.models import User
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)

class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, request: RegisterRequest) -> UserResponse:
        existing_user_by_email = self.user_repository.get_by_email(request.email)
        if existing_user_by_email:
            raise EmailAlreadyExistsException("Email already exists")

        existing_user_by_username = self.user_repository.get_by_username(request.username)
        if existing_user_by_username:
            raise UsernameAlreadyExistsException("Username already exists")

        hashed_password = hash_password(request.password)

        new_user = User(
            full_name=request.full_name,
            email=request.email,
            username=request.username,
            password=hashed_password
        )

        created_user = self.user_repository.create(new_user)

        return UserResponse.model_validate(created_user)
    
    def login(self, request: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(request.identifier) or self.user_repository.get_by_username(request.identifier)
        if not user or not verify_password(request.password, user.password):
            raise InvalidCredentialsException("Invalid credentials")
        
        if not verify_password(request.password, user.password):
            raise InvalidCredentialsException("Invalid credentials")
        
        if not user.is_active:
            raise InvalidCredentialsException("User is not active")
        
        if not user.is_verified:
            raise InvalidCredentialsException("User is not verified")
        
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id)
        )