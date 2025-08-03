from fastapi import Request
from fastapi.responses import JSONResponse

from redirector.api.base import app
from redirector.exceptions.user import UserNotFoundException


@app.exception_handler(UserNotFoundException)
def link_not_found(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"},
    )
