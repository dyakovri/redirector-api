from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl


class NewRedirectUrl(BaseModel):
    url_to: AnyHttpUrl
