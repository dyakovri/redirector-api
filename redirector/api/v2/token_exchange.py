import logging
import random
import string
from typing import Annotated, Any

from aiohttp import ClientSession
from fastapi import APIRouter, Query, Request
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
from fastapi_sqlalchemy import db
from pydantic import BaseModel

from redirector.api.auth import auth_user
from redirector.models.user import User
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


async def add_user_to_db(user_claims: dict[str, Any]) -> User:
    sub = user_claims.get("sub")
    if not sub:
        raise ValueError("No subject in token")

    user = db.session.query(User).filter(User.username == sub).one_or_none()
    if not user:
        user = User()

    user.username = sub
    user.email = user_claims.get("email")
    user.full_name = (
        user_claims.get("name")
        or user_claims.get("given_name")
        or user_claims.get("full_name")
        or user_claims.get("preferred_username")
        or user_claims.get("nickname")
    )
    db.session.merge(user)
    db.session.commit()
    return user


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
    if "access_token" not in token_data:
        return RedirectResponse("/ui/?error=Invalid%20auth%20response")
    user_claims = auth_user.decode_token(token_data["access_token"])

    logger.debug("Got token for user %s: %s*** ", user_claims["sub"], token_data["access_token"][:10])
    try:
        await add_user_to_db(user_claims)
    except ValueError:
        return RedirectResponse("/ui/?error=No%20subject%20in%20token")

    return RedirectResponse(f"/ui/?token={token_data['access_token']}&expires_in={token_data.get('expires_in', -1)}")
