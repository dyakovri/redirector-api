from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi_sqlalchemy import db
from starlette.responses import RedirectResponse, Response

from .models import Link
from .schemas import NewRedirectUrl
from .settings import get_settings


router = APIRouter()


@router.post("/{secret}/url/{url_from:path}", status_code=201)
def create_route(secret: str, url_from: str, data: NewRedirectUrl):
    if secret != get_settings().SECRET:
        raise HTTPException(403, "Wrong secret")
    if db.session.query(Link).filter(Link.url_from == url_from).one_or_none():
        raise HTTPException(409, "Already exists")
    redir_obj = Link(url_from=url_from, url_to=data.url_to)
    db.session.add(redir_obj)
    db.session.commit()
    return "ok"


@router.delete("/{secret}/url/{url_from:path}", status_code=204)
def create_route(secret: str, url_from: str):
    if secret != get_settings().SECRET:
        raise HTTPException(403, "Wrong secret")
    redir_obj = (
        db.session.query(Link).filter(Link.url_from == url_from).one_or_none()
    )
    if not redir_obj:
        raise HTTPException(404, "Not found")
    db.session.delete(redir_obj)
    db.session.commit()
    return Response(status_code=204)


def log_redirect():
    pass


@router.api_route(
    "/{url_from:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    status_code=307,
)
def redirect(url_from: str, background_tasks: BackgroundTasks):
    if url_from == '':
        return RedirectResponse('/ui/')
    redir_obj = (
        db.session.query(Link).filter(Link.url_from == url_from).one_or_none()
    )
    if not redir_obj:
        raise HTTPException(404, "Not found")

    background_tasks.add_task(log_redirect)
    return RedirectResponse(redir_obj.url_to)
