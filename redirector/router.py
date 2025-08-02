from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi_sqlalchemy import db
from starlette.responses import RedirectResponse, Response
import user_agents

from .models import Link, RedirectFact
from .schemas import NewRedirectUrl
from .settings import get_settings


router = APIRouter()


@router.post("/{secret}/url/{url_from:path}", status_code=201)
def create_route(secret: str, url_from: str, data: NewRedirectUrl):
    if secret != get_settings().SECRET:
        raise HTTPException(403, "Wrong secret")
    if db.session.query(Link).filter(Link.url_from == url_from).one_or_none():
        raise HTTPException(409, "Already exists")
    redir_obj = Link()
    redir_obj.url_from=url_from
    redir_obj.url_to=str(data.url_to)
    db.session.add(redir_obj)
    db.session.commit()
    return "ok"


@router.delete("/{secret}/url/{url_from:path}", status_code=204)
def delete_route(secret: str, url_from: str):
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


def log_redirect(link_id, method, user_agent):
    ua = user_agents.parse(user_agent)
    fact = RedirectFact()
    fact.link_id = link_id
    fact.method = method
    fact.user_agent = user_agent
    fact.browser_family = ua.browser.family
    fact.browser_version = ua.browser.version_string
    fact.os_family = ua.os.family
    fact.os_version = ua.os.version_string
    fact.device_family = ua.device.family
    fact.device_brand = ua.device.brand
    fact.device_model = ua.device.model
    db.session.add(fact)
    db.session.commit()


@router.api_route(
    "/{url_from:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    status_code=307,
)
def redirect(request: Request, url_from: str, background_tasks: BackgroundTasks):
    if url_from == '':
        return RedirectResponse('/ui/')
    redir_obj = (
        db.session.query(Link).filter(Link.url_from == url_from).one_or_none()
    )
    if not redir_obj:
        raise HTTPException(404, "Not found")

    background_tasks.add_task(log_redirect, redir_obj.id, request.method, request.headers["User-Agent"])
    return RedirectResponse(redir_obj.url_to)
