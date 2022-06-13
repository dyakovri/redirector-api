import logging
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redirector.settings import get_settings


logger = logging.getLogger(__name__)
auth_schema = HTTPBearer(bearerFormat="JWT")


def validate_user(token: HTTPAuthorizationCredentials):
    logger.debug(token.credentials)
    if token.credentials != get_settings().SECRET:
        raise HTTPException(403, "Wrong secret")
    return "Unregistred"
