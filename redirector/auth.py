import logging

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_sqlalchemy import db

from redirector.models import RedirectorUser
from redirector.settings import get_settings

logger = logging.getLogger(__name__)
auth_schema = HTTPBearer(bearerFormat="JWT")


def validate_user(token: HTTPAuthorizationCredentials) -> RedirectorUser:
    if token.credentials != get_settings().SECRET:
        raise HTTPException(403, "Wrong secret")
    return db.session.query(RedirectorUser).get(0)
