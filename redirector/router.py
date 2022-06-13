from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from starlette.responses import RedirectResponse, Response

from .auth import validate_user, auth_schema
from .models import Redirect
from .schemas import NewRedirectUrl
from .settings import get_settings


router = APIRouter()


@router.post("/url/{url_from:path}", status_code=201)
def create_route(
    url_from: str, data: NewRedirectUrl, secret: str = Depends(auth_schema)
):
    user = validate_user(secret)
    if db.session.query(Redirect).filter(Redirect.url_from == url_from).one_or_none():
        raise HTTPException(409, "Already exists")
    redir_obj = Redirect(url_from=url_from, url_to=data.url_to)
    db.session.add(redir_obj)
    db.session.commit()
    return "ok"


@router.delete("/url/{url_from:path}", status_code=204)
def create_route(url_from: str, secret: str = Depends(auth_schema)):
    user = validate_user(secret)
    redir_obj = (
        db.session.query(Redirect).filter(Redirect.url_from == url_from).one_or_none()
    )
    if not redir_obj:
        raise HTTPException(404, "Not found")
    db.session.delete(redir_obj)
    db.session.commit()
    return Response(status_code=204)


@router.api_route(
    "/{url_from:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    status_code=307,
)
def redirect(url_from):
    if url_from == "":
        return RedirectResponse("/ui/")
    redir_obj = (
        db.session.query(Redirect).filter(Redirect.url_from == url_from).one_or_none()
    )
    if not redir_obj:
        raise HTTPException(404, "Not found")
    return RedirectResponse(redir_obj.url_to)
