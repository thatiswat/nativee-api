from fastapi import APIRouter

from app.routes.analytics import router as analytics_router
from app.routes.api_keys import router as api_keys_router
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.me import router as me_router
from app.routes.plans import router as plans_router
from app.routes.project_dashboard import router as project_dashboard_router
from app.routes.projects import router as projects_router
from app.routes.speech import router as speech_router
from app.routes.translate import router as translate_router
from app.routes.usage import router as usage_router

router = APIRouter(prefix="/v1")

# Core APIs
router.include_router(speech_router)
router.include_router(translate_router)

# Authentication
router.include_router(auth_router)

# Customer Console
router.include_router(dashboard_router)
router.include_router(projects_router)

# Project Console
router.include_router(project_dashboard_router)
router.include_router(api_keys_router)
router.include_router(usage_router)
router.include_router(analytics_router)
router.include_router(me_router)

# Platform
router.include_router(plans_router)


@router.get("/health", tags=["Platform"])
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
    }