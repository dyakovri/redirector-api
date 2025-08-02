from .base import app
from .redirects import router as redirects_router
from .v1 import router as v1_router


app.include_router(redirects_router, include_in_schema=False)
app.include_router(v1_router, deprecated=True)
