from datetime import datetime
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from redirector.exceptions.link import LinkNotFoundException, LinkAlreadyExistsException
from redirector.models import Link
from pydantic import AnyHttpUrl, BaseModel, TypeAdapter

router = APIRouter()


# GET
class LinkResponse(BaseModel):
    url_from: AnyHttpUrl | str
    url_to: AnyHttpUrl
    created_at: datetime
    updated_at: datetime


class LinkListResponse(BaseModel):
    items: list[LinkResponse]


@router.get("")
async def get_links() -> LinkListResponse:
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


@router.put("")
async def create_link(json: PostLinkRequest) -> PostLinkResponse:
    new_link = db.session.query(Link).filter(Link.url_from == str(json.url_from)).one_or_none()
    if new_link is not None and not json.force:
        raise LinkAlreadyExistsException(json.url_from)
    new_link = new_link or Link()
    new_link.url_from = str(json.url_from)
    new_link.url_to = str(json.url_to)
    db.session.add(new_link)
    db.session.commit()
    return PostLinkResponse.model_validate(new_link, from_attributes=True)


# DELETE
class DeleteLinkRequest(BaseModel):
    url_from: AnyHttpUrl | str


@router.delete("", status_code=204)
async def delete_link(json: DeleteLinkRequest):
    link = db.session.query(Link).filter(Link.url_from == str(json.url_from)).one_or_none()
    if not link:
        raise LinkNotFoundException(json.url_from)
    db.session.delete(link)
    db.session.commit()
    return
