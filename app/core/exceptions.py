class AppException(Exception):

    status_code = 400

    message = "Application Error"

    def __init__(
        self,
        message: str | None = None,
    ):
        self.message = message or self.message


class BadRequestException(AppException):
    status_code = 400
    message = "Bad Request"


class UnauthorizedException(AppException):
    status_code = 401
    message = "Unauthorized"


class ForbiddenException(AppException):
    status_code = 403
    message = "Forbidden"


class NotFoundException(AppException):
    status_code = 404
    message = "Not Found"


class ConflictException(AppException):
    status_code = 409
    message = "Conflict"


class InternalServerException(AppException):
    status_code = 500
    message = "Internal Server Error"