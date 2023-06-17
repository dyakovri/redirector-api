from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.orm import relationship


@as_declarative()
class BaseModel:
    pass


class Link(BaseModel):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    url_from = Column(String, nullable=False, unique=True)
    url_to = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    redirects = relationship("RedirectFact", back_populates="link")


class RedirectFact(BaseModel):
    __tablename__ = "redirect_fact"

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("link.id"))
    method = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user_agent = Column(String, nullable=False)

    browser_family = Column(String, nullable=False)
    browser_version = Column(String, nullable=False)

    os_family = Column(String, nullable=False)
    os_version = Column(String, nullable=False)

    device_family = Column(String, nullable=False)
    device_brand = Column(String, nullable=False)
    device_model = Column(String, nullable=False)

    link = relationship("Link", back_populates="redirects")
