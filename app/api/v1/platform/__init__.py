from fastapi import APIRouter

from app.api.v1.platform.health import router as health_router
from app.api.v1.platform.version import router as version_router
from app.api.v1.platform.plans import router as plans_router

router = APIRouter(
    prefix="/platform",
    tags=["Platform"],
)

router.include_router(health_router)
router.include_router(version_router)
router.include_router(plans_router)