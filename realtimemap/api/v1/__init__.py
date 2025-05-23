__all__ = ["router"]

from fastapi import APIRouter

from core.config import conf
from .auth import router as auth_router
from .mark import router as mark_router

router = APIRouter(prefix=conf.api.v1.prefix)
router.include_router(auth_router)
router.include_router(mark_router)
