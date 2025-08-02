from fastapi import APIRouter

from redirector.settings import get_settings

router = APIRouter()
settings = get_settings()
