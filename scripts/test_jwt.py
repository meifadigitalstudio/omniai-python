from app.auth.jwt import (
    create_access_token,
    decode_token,
)

token = create_access_token(
    "123456789"
)

print(token)

print()

print(
    decode_token(token)
)