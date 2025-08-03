import logging
from typing import Annotated, NamedTuple

from fastapi import Depends
from fastapi_auth_oidc import IDToken, OIDCProvider
from fastapi_auth_oidc.exceptions import InvalidCredentialsException, UnauthenticatedException

from redirector.settings import get_settings

__all__ = [
    "AUTH_RESPONSES",
    "AUTH_RESPONSES_AUTHENTICATION",
    "AUTH_RESPONSES_AUTHORIZATION",
    "InvalidCredentialsException",
    "UnauthenticatedException",
    "ForbiddenException",
    "User",
]


AUTH_RESPONSES_AUTHENTICATION = {401: {"description": "Client needs to log in or renew token"}}
AUTH_RESPONSES_AUTHORIZATION = {403: {"description": "Client is authenticated but lacks the necessary permissions"}}
AUTH_RESPONSES = {
    **AUTH_RESPONSES_AUTHENTICATION,
    **AUTH_RESPONSES_AUTHORIZATION,
}

logger = logging.getLogger(__name__)
settings = get_settings()
auth_user = OIDCProvider(
    configuration_uri=str(settings.oidc_configuration_uri),
    client_id=settings.oidc_client_id,
    token_type=IDToken,
)
TokenData = Annotated[IDToken | None, Depends(auth_user)]


class ForbiddenException(Exception):
    pass


def get_authenticated(user: TokenData):
    if not user:
        raise UnauthenticatedException()
    return user


def is_admin(user: IDToken):
    claim_value = user.model_dump().get(settings.oidc_admin_claim)
    logger.debug(
        "Claim `%s` value: %s (shoud be %s)",
        settings.oidc_admin_claim,
        claim_value,
        settings.oidc_admin_claim_value,
    )
    return (isinstance(claim_value, list) and settings.oidc_admin_claim_value in claim_value) or (
        not isinstance(claim_value, list) and settings.oidc_admin_claim_value == claim_value
    )


def get_is_admin(user: Annotated[IDToken, Depends(get_authenticated)]):
    if is_admin(user):
        raise ForbiddenException(user, settings.oidc_admin_claim, settings.oidc_admin_claim_value)
    return user


class User(NamedTuple):
    authenticated = Annotated[IDToken, Depends(get_authenticated)]
    is_admin = Annotated[IDToken, Depends(get_is_admin)]
