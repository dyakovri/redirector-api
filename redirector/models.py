from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql.sqltypes import DateTime, Integer, String


@as_declarative()
class BaseModel:
    pass


class Redirect(BaseModel):
    __tablename__ = "redirects"

    id = Column(Integer, primary_key=True)
    url_from = Column(String, nullable=False, unique=True)
    url_to = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
