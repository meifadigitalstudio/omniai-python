from app.core import (
    ConflictException,
    BadRequestException,
)


class EmailAlreadyExistsException(
    ConflictException,
):
    message = "Email already exists."


class UsernameAlreadyExistsException(
    ConflictException,
):
    message = "Username already exists."


class InvalidCredentialsException(
    BadRequestException,
):
    message = "Invalid email or password."