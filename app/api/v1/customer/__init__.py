from fastapi import APIRouter

from .auth import router as auth_router
from .projects import router as projects_router
from .project_dashboard import router as project_dashboard_router
from .dashboard import router as dashboard_router
from .api_keys import router as api_keys_router
from .analytics import router as analytics_router
from .usage import router as usage_router
from .profile import router as profile_router

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)

router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(projects_router)
router.include_router(project_dashboard_router)
router.include_router(dashboard_router)
router.include_router(api_keys_router)
router.include_router(analytics_router)
router.include_router(usage_router)