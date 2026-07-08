from fastapi import APIRouter

from app.api.platform.health import router as health_router
from app.api.platform.version import router as version_router
from app.api.platform.plans import router as plans_router
from app.api.platform.ai import router as ai_router
from app.api.platform.console import router as console_router


router = APIRouter()


router.include_router(health_router)
router.include_router(version_router)
router.include_router(plans_router)
router.include_router(ai_router)
router.include_router(console_router)