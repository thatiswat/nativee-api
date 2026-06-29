from fastapi import APIRouter

from app.routes.speech import router as speech_router
from app.routes.translate import router as translate_router
from app.routes.api_keys import router as api_key_router
from app.routes.analytics import router as analytics_router
from app.routes.plans import router as plans_router
from app.routes.usage import router as usage_router
from app.routes.me import router as me_router
from app.routes.dashboard import router as dashboard_router  # ✅ ADDED


router = APIRouter(prefix="/v1")

# -------------------------
# Core feature routes
# -------------------------
router.include_router(speech_router)
router.include_router(translate_router)
router.include_router(api_key_router)
router.include_router(analytics_router)
router.include_router(plans_router)
router.include_router(usage_router)
router.include_router(me_router)
router.include_router(dashboard_router)  # ✅ ADDED

# -------------------------
# Health check
# -------------------------
@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
    }