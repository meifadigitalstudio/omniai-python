from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.router import router
from app.core import settings

from app.core import AppException
from app.utils import error_response

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(router)


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.message,
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = {}

    for error in exc.errors():

        field = ".".join(
            map(str, error["loc"][1:])
        )

        errors.setdefault(field, []).append(
            error["msg"]
        )

    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Validation Error",
            errors=errors,
        ).model_dump(),
    )

@app.exception_handler(Exception)
async def exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Internal Server Error",
        ).model_dump(),
    )