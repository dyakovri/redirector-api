from typing import Annotated, NamedTuple

from fastapi import Depends
from fastapi_auth_oidc import IDToken, OIDCProvider
from fastapi_auth_oidc.exceptions import InvalidCredentialsException, UnauthenticatedException

from redirector.settings import get_settings


__all__ = ["InvalidCredentialsException", "UnauthenticatedException", "ForbiddenException", "User"]


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


def get_is_admin(user: Annotated[IDToken, Depends(get_authenticated)]):
    claim_value = user.model_dump().get(settings.oidc_admin_claim)
    if (not isinstance(claim_value, list) and claim_value != settings.oidc_admin_claim_value) or (
        isinstance(claim_value, list) and settings.oidc_admin_claim_value not in claim_value
    ):
        raise ForbiddenException(user, settings.oidc_admin_claim, claim_value, settings.oidc_admin_claim_value)
    return user


class User(NamedTuple):
    authenticated = Annotated[IDToken, Depends(get_authenticated)]
    is_admin = Annotated[IDToken, Depends(get_is_admin)]
