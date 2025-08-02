from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from redirector.settings import get_settings

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=str(get_settings().DB_DSN))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
