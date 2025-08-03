from fastapi import Request
from fastapi.responses import JSONResponse

from .auth import ForbiddenException, InvalidCredentialsException, UnauthenticatedException
from .base import app


@app.exception_handler(UnauthenticatedException)
def invalid_credentials(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid token"},
    )


@app.exception_handler(InvalidCredentialsException)
def not_authenticated(request: Request, exc: UnauthenticatedException):
    return JSONResponse(
        status_code=401,
        content={"detail": "Token not valid"},
    )


@app.exception_handler(ForbiddenException)
def not_authorized(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=403,
        content={"detail": "Token not valid"},
    )
