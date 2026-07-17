from app.common.responses.schemas import (
    ApiResponse,
    ErrorResponse,
    Meta,
    PaginatedResponse,
)


def success_response(
    *,
    data,
    message: str = "Success",
):
    return ApiResponse(
        success=True,
        message=message,
        data=data,
    )


def created_response(
    *,
    data,
    message: str,
):
    return ApiResponse(
        success=True,
        message=message,
        data=data,
    )


def paginated_response(
    *,
    data,
    meta: Meta,
    message: str = "Success",
):
    return PaginatedResponse(
        success=True,
        message=message,
        data=data,
        meta=meta,
    )


def error_response(
    *,
    message: str,
    errors=None,
):
    return ErrorResponse(
        success=False,
        message=message,
        errors=errors,
    )
