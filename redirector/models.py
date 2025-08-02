from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, mapped_column, Mapped


@as_declarative()
class BaseModel:
    pass


class Link(BaseModel):
    __tablename__ = "link"

    id: Mapped[int] = mapped_column(primary_key=True)
    url_from: Mapped[str] = mapped_column(unique=True)
    url_to: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    redirects = relationship("RedirectFact", back_populates="link")


class RedirectFact(BaseModel):
    __tablename__ = "redirect_fact"

    id: Mapped[int] = mapped_column(primary_key=True)
    link_id: Mapped[str] = mapped_column(ForeignKey("link.id"))
    method: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_agent: Mapped[str]

    browser_family: Mapped[str | None]
    browser_version: Mapped[str | None]

    os_family: Mapped[str | None]
    os_version: Mapped[str | None]

    device_family: Mapped[str | None]
    device_brand: Mapped[str | None]
    device_model: Mapped[str | None]

    link = relationship("Link", back_populates="redirects")
