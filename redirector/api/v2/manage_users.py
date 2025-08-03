from fastapi import APIRouter

from redirector.api.auth import User

router = APIRouter()


@router.get("/me")
def get_me(
    user: User.authenticated,
):
    return user.model_dump() if user else {}
