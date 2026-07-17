from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import token
from uuid import uuid4

import jwt

from app.core import settings

@dataclass
class TokenData:
    token: str
    expires_at: datetime
    
def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
) -> TokenData:

    now = datetime.now(timezone.utc)
    expires_at = now + expires_delta

    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": expires_at,
        "jti": str(uuid4()),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return TokenData(
        token=token,
        expires_at=expires_at,
    )


def create_access_token(
    subject: str,
) -> TokenData:

    return _create_token(
        subject,
        "access",
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )


def create_refresh_token(
    subject: str,
) -> TokenData:

    return _create_token(
        subject,
        "refresh",
        timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    )


def decode_token(
    token: str,
):

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )