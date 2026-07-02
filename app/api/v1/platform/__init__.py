from fastapi import APIRouter

from .plans import router as plans_router

router = APIRouter(
    prefix="/platform",
    tags=["Platform"],
)

router.include_router(plans_router)