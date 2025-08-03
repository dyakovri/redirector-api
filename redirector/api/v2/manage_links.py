from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_sqlalchemy import db
from pydantic import AnyHttpUrl, BaseModel, TypeAdapter

from redirector.api.auth import User
from redirector.exceptions.link import LinkAlreadyExistsException, LinkNotFoundException
from redirector.models import Link

router = APIRouter()


# GET
class LinkRequest(BaseModel):
    my: bool = False
    user: str | None = None


class LinkResponse(BaseModel):
    url_from: AnyHttpUrl | str
    url_to: AnyHttpUrl
    created_at: datetime
    updated_at: datetime


class LinkListResponse(BaseModel):
    items: list[LinkResponse]


@router.get("")
async def get_links(
    query: Annotated[LinkRequest, Query()],
    user: User.authenticated,
) -> LinkListResponse:
    links = db.session.query(Link).all()
    return LinkListResponse(
        items=TypeAdapter(list[LinkResponse]).validate_python(links, from_attributes=True),
    )


# CREATE OR UPDATE
class PostLinkRequest(BaseModel):
    url_from: AnyHttpUrl
    url_to: AnyHttpUrl
    force: bool = False


class PostLinkResponse(LinkResponse):
    pass


@router.put("", status_code=201)
async def create_link(
    body: PostLinkRequest,
    user: User.authenticated,
) -> PostLinkResponse:
    new_link = db.session.query(Link).filter(Link.url_from == str(body.url_from)).one_or_none()
    if new_link is not None and not body.force:
        raise LinkAlreadyExistsException(body.url_from)
    new_link = new_link or Link()
    new_link.url_from = str(body.url_from)
    new_link.url_to = str(body.url_to)
    db.session.add(new_link)
    db.session.commit()
    return PostLinkResponse.model_validate(new_link, from_attributes=True)


# DELETE
class DeleteLinkRequest(BaseModel):
    url_from: AnyHttpUrl | str


@router.delete("", status_code=204)
async def delete_link(
    body: DeleteLinkRequest,
    user: User.authenticated,
):
    link = db.session.query(Link).filter(Link.url_from == str(body.url_from)).one_or_none()
    if not link:
        raise LinkNotFoundException(body.url_from)
    db.session.delete(link)
    db.session.commit()
    return
