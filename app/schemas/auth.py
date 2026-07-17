from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(
        min_length=3,
        max_length=150,
    )
    username: str = Field(
        min_length=3,
        max_length=50,
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=255,
    )


class LoginRequest(BaseModel):
    identifier: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str
    full_name: str
    username: str
    email: EmailStr
    avatar_url: str | None
    phone_number: str | None
    is_active: bool
    is_verified: bool