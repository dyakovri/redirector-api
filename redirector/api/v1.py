from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl
from starlette.responses import Response

from redirector.models import Link
from redirector.settings import get_settings

router = APIRouter()


class NewRedirectUrl(BaseModel):
    url_to: AnyHttpUrl


@router.post("/{secret}/url/{url_from:path}", status_code=201)
def create_route(secret: str, url_from: str, data: NewRedirectUrl):
    if secret != get_settings().secret:
        raise HTTPException(403, "Wrong secret")
    if db.session.query(Link).filter(Link.url_from == url_from).one_or_none():
        raise HTTPException(409, "Already exists")
    redir_obj = Link()
    redir_obj.url_from = url_from
    redir_obj.url_to = str(data.url_to)
    db.session.add(redir_obj)
    db.session.commit()
    return "ok"


@router.delete("/{secret}/url/{url_from:path}", status_code=204)
def delete_route(secret: str, url_from: str):
    if secret != get_settings().secret:
        raise HTTPException(403, "Wrong secret")
    redir_obj = db.session.query(Link).filter(Link.url_from == url_from).one_or_none()
    if not redir_obj:
        raise HTTPException(404, "Not found")
    db.session.delete(redir_obj)
    db.session.commit()
    return Response(status_code=204)
