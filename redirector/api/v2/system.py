from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import text

from redirector import __version__
from redirector.settings import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/configuration")
def get_configuration():
    return {
        "version": __version__,
        "domains": settings.allowed_domains,
    }


@router.get("/liveness")
def liveness_probe():
    return {"status": "ok"}


@router.get("/readiness")
def readiness_probe():
    status = True
    probes = []

    try:
        db.session.execute(text("SELECT 1"))
    except Exception as exc:
        status = False
        probes.append({"system": "db", "status": "error", "details": str(exc)})

    return {"status": "ok" if status else "error", "probes": probes}
