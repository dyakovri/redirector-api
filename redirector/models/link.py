"""Link management ORM models."""

from datetime import datetime

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Link(BaseModel):
    __tablename__ = "link"
    __table_args__ = (
        Index("idx__link__url_from", "url_from", postgresql_using="hash"),
        Index("idx__link__owner_id", "owner_id", postgresql_using="hash"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    url_from: Mapped[str] = mapped_column(unique=True)
    url_to: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    redirects = relationship("RedirectFact", back_populates="link")
    owner = relationship("User", back_populates="links")


class RedirectFact(BaseModel):
    __tablename__ = "redirect_fact"
    __table_args__ = (Index("idx__redirect_fact__link_id", "link_id", "created_at"),)

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
