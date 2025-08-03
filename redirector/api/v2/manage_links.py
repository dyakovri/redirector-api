from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_sqlalchemy import db
from pydantic import AnyHttpUrl, BaseModel, TypeAdapter
from typing_extensions import Doc

from redirector.api.auth import AUTH_RESPONSES, AUTH_RESPONSES_AUTHENTICATION, ForbiddenException, User, is_admin
from redirector.exceptions.link import LinkAlreadyExistsException, LinkNotFoundException
from redirector.models import Link
from redirector.models import User as DbUser

router = APIRouter()


# GET
class LinkRequest(BaseModel):
    my: Annotated[bool, Doc("Get only your links if you are an admin")] = False
    user: str | None = None


class OwnerResponse(BaseModel):
    id: int
    username: str
    email: str | None
    full_name: str | None


class LinkResponse(BaseModel):
    url_from: AnyHttpUrl | str
    url_to: AnyHttpUrl
    owner: OwnerResponse
    created_at: datetime
    updated_at: datetime


class LinkListResponse(BaseModel):
    items: list[LinkResponse]


@router.get(
    "",
    responses={**AUTH_RESPONSES},
)
async def get_links(
    query: Annotated[LinkRequest, Query()],
    user: User.authenticated,
) -> LinkListResponse:
    links_request = db.session.query(Link)
    user_is_admin = is_admin(user)
    query.my = query.my or not user_is_admin

    if query.my:
        links_request = links_request.join(Link.owner).filter(DbUser.username == user.sub)

    if query.user and user_is_admin:
        links_request = links_request.join(Link.owner).filter(DbUser.username == query.user)
    elif query.user:
        raise ForbiddenException(user)

    links = links_request.all()
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


@router.put(
    "",
    status_code=201,
    responses={**AUTH_RESPONSES_AUTHENTICATION},
)
async def create_link(
    body: PostLinkRequest,
    user: User.authenticated,
) -> PostLinkResponse:
    new_link = db.session.query(Link).filter(Link.url_from == str(body.url_from)).one_or_none()
    current_user_id = db.session.query(DbUser).filter(DbUser.username == user.sub).one().id

    if new_link is not None and not body.force:
        raise LinkAlreadyExistsException(body.url_from)
    if new_link is not None and body.force and (new_link.owner_id != current_user_id or not is_admin(user)):
        raise ForbiddenException(user)

    new_link = new_link or Link()
    new_link.url_from = str(body.url_from)
    new_link.url_to = str(body.url_to)
    new_link.owner_id = current_user_id

    db.session.add(new_link)
    db.session.commit()
    return PostLinkResponse.model_validate(new_link, from_attributes=True)


# DELETE
class DeleteLinkRequest(BaseModel):
    url_from: AnyHttpUrl | str


@router.delete(
    "",
    status_code=204,
    responses={**AUTH_RESPONSES},
)
async def delete_link(
    body: DeleteLinkRequest,
    user: User.authenticated,
):
    """Removes your link by its `url_from`.

    If you are an admin, you can delete any link.
    """
    link = db.session.query(Link).filter(Link.url_from == str(body.url_from)).one_or_none()
    if not link:
        raise LinkNotFoundException(body.url_from)
    if not is_admin(user) and link.owner.username != user.sub:
        raise ForbiddenException(user)
    db.session.delete(link)
    db.session.commit()
    return
