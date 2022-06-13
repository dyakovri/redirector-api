import logging

import jwt

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_sqlalchemy import db

from redirector.models import RedirectorUser
from redirector.settings import get_settings

logger = logging.getLogger(__name__)
auth_schema = HTTPBearer(bearerFormat="JWT")


def validate_user(token: HTTPAuthorizationCredentials) -> RedirectorUser:
    try:
        userdata = jwt.decode(
            token.credentials, key=get_settings().JWT_SECRET, algorithms=["HS256"]
        )
    except jwt.DecodeError:
        raise HTTPException(403, "Wrong secret")
    user = (
        db.session.query(RedirectorUser)
        .filter(RedirectorUser.username == userdata["username"])
        .one_or_none()
    )
    if not user:
        user = RedirectorUser(username=userdata["username"])
        db.session.add(user)
        db.session.flush()
    return user
