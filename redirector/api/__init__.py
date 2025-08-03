from fastapi import APIRouter

from . import auth_exceptions  # noqa: F401
from .base import app
from .redirects import router as redirects_router
from .v1 import router as api_v1_router
from .v2 import manage_links_exceptions  # noqa: F401
from .v2.manage_links import router as manage_links_router
from .v2.manage_users import router as manage_users_router
from .v2.system import router as system_router
from .v2.token_exchange import router as token_exchange_router

api_router = APIRouter(prefix="/api")
api_router.include_router(system_router, prefix="/system", tags=["System"], include_in_schema=False)

# v2 routers
api_v2_router = APIRouter(prefix="/v2")
api_v2_router.include_router(manage_links_router, prefix="/link", tags=["Link"])
api_v2_router.include_router(manage_users_router, prefix="/user", tags=["User"])
api_v2_router.include_router(token_exchange_router, prefix="/oidc", tags=["OIDC"])
api_router.include_router(api_v2_router)

app.include_router(api_router)

# legacy routes
app.include_router(api_v1_router, tags=["Legacy"], deprecated=True)

# Redirects
# Должен быть последним
app.include_router(redirects_router, tags=["Redirects"], include_in_schema=False)
