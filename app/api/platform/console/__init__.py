from fastapi import APIRouter

from .analytics import router as analytics_router
from .api_keys import router as api_keys_router
from .dashboard import router as dashboard_router
from .profile import router as profile_router
from .project_dashboard import router as project_dashboard_router
from .projects import router as projects_router

router = APIRouter(
    prefix="/console",
)

router.include_router(dashboard_router)
router.include_router(projects_router)
router.include_router(api_keys_router)
router.include_router(analytics_router)
router.include_router(project_dashboard_router)
router.include_router(profile_router)