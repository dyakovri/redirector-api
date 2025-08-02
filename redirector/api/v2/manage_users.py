from typing import Annotated
from fastapi import APIRouter, Depends


from redirector.api.auth import IDToken, auth_user

router = APIRouter()


@router.get("/me")
def get_me(
    user: Annotated[IDToken | None, Depends(auth_user)],
):
    return user.model_dump() if user else {}
