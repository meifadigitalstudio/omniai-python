from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from app.core.config import settings


def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
        "jti": str(uuid4()),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(
    subject: str,
) -> str:

    return _create_token(
        subject,
        "access",
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )


def create_refresh_token(
    subject: str,
) -> str:

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