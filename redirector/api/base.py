from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from redirector import __version__
from redirector.settings import get_settings

settings = get_settings()


app = FastAPI(
    title="Redirector",
    description="App to shorten, brand and track links",
    version=__version__,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
    swagger_ui_parameters={"persistAuthorization": True},
)
app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.db_dsn),
    engine_args={"pool_pre_ping": True},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
