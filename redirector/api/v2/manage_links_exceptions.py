from fastapi import Request
from fastapi.responses import JSONResponse

from redirector.api.base import app
from redirector.exceptions.link import LinkAlreadyExistsException, LinkDomainNotAllowedException, LinkNotFoundException


@app.exception_handler(LinkNotFoundException)
def link_not_found(request: Request, exc: LinkNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Link not found"},
    )


@app.exception_handler(LinkAlreadyExistsException)
def link_already_exists(request: Request, exc: LinkAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"detail": "Link already exists"},
    )


@app.exception_handler(LinkDomainNotAllowedException)
def link_domain_not_allowed(request: Request, exc: LinkDomainNotAllowedException):
    return JSONResponse(
        status_code=406,
        content={"detail": "Domain not allowed"},
    )
