from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from .router import router
from .settings import get_settings

app = FastAPI()
app.add_middleware(
    DBSessionMiddleware,
    db_url=str(get_settings().DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
