"""User management ORM models."""

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    __table_args__ = (Index("idx__user__username", "username", postgresql_using="hash"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str | None]
    full_name: Mapped[str | None]

    links = relationship("Link", back_populates="owner")
