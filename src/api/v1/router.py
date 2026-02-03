from fastapi import APIRouter

from .endpoints import deals

router = APIRouter(prefix="/v1")
router.include_router(deals.router)
