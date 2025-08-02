import user_agents
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi_sqlalchemy import db
from sqlalchemy import or_

from redirector.models import Link, RedirectFact

router = APIRouter()


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
    if url_from == "":
        return RedirectResponse("/ui/")
    possible_redirects = (
        db.session.query(Link)
        .filter(
            or_(
                Link.url_from == url_from,
                Link.url_from == str(request.url),
            )
        )
        .all()
    )
    final_redirect = None
    if len(possible_redirects) == 0:
        raise HTTPException(404, "Not found")
    if len(possible_redirects) > 1:
        for obj in possible_redirects:
            if obj.url_from == str(request.url):
                # Нашли домен-специфичный, дальше не ищем
                final_redirect = obj
                break
            if obj.url_from == url_from:
                # Нашли общий, но продолжаем искать домен-специфичный
                final_redirect = obj

    if final_redirect is None:
        raise HTTPException(404, "Not found")

    background_tasks.add_task(log_redirect, final_redirect.id, request.method, request.headers["User-Agent"])
    return RedirectResponse(final_redirect.url_to)
