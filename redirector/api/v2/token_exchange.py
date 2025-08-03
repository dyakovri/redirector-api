import logging
import random
import string
from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Query, Request
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from redirector.api.auth import auth_user
from redirector.settings import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


@router.get("/auth")
async def token_request(
    request: Request,
):
    state = "".join(random.choice(string.ascii_letters) for i in range(32))
    url = URL(auth_user.authorization_endpoint).include_query_params(
        response_type="code",
        client_id=settings.oidc_client_id,
        redirect_uri=f"{request.url.scheme}://{request.url.netloc}/api/v2/oidc/redirect",
        state=state,
        scopes="openid",
        optional_scopes="email profile",
    )
    logger.debug("Redirecting to %s", url)
    return RedirectResponse(url)


class AuthorizationCodeRedirectParams(BaseModel):
    code: str | None = None

    error: str | None = None
    error_description: str | None = None

    state: str | None = None


@router.get("/redirect")
async def token_redirect(
    request: Request,
    query: Annotated[AuthorizationCodeRedirectParams, Query()],
):
    if not query.code:
        return RedirectResponse(f"/ui/?error={query.error_description}")
    token_request_data = {
        "grant_type": "authorization_code",
        "code": query.code,
        "redirect_uri": f"{request.url.scheme}://{request.url.netloc}{request.url.path}",
        "client_id": settings.oidc_client_id,
        "client_secret": settings.oidc_client_secret,
    }
    logger.debug("Request to %s for token", auth_user.token_endpoint)
    async with (
        ClientSession() as session,
        session.post(auth_user.token_endpoint, data=token_request_data) as response,
    ):
        token_data = await response.json()
    if "access_token" in token_data:
        return RedirectResponse(
            f"/ui/?token={token_data['access_token']}&expires_in={token_data.get('expires_in', -1)}"
        )
    else:
        return RedirectResponse("/ui/?error=Invalid%20auth%20response")
