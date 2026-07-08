from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.platform.dashboard import (
    DashboardTimeRange,
    ProjectDashboardResponse,
)
from app.schemas.platform.error import ErrorResponse
from app.services.platform.project_dashboard import ProjectDashboardService

router = APIRouter(
    prefix="/project-dashboard",
    tags=["Project Dashboard"],
)


@router.get(
    "/{project_id}",
    response_model=ProjectDashboardResponse,
    summary="Project Dashboard",
    description="""
Returns dashboard statistics for a project owned by the authenticated user.

Includes:

- Total requests
- Requests today
- Average latency
- Success rate
""",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        },
        403: {
            "model": ErrorResponse,
            "description": "Forbidden",
        },
        404: {
            "model": ErrorResponse,
            "description": "Project not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def get_dashboard(
    project_id: int,
    time_range: DashboardTimeRange = DashboardTimeRange.LAST_24_HOURS,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProjectDashboardService(db)

    return service.overview(
        user=current_user,
        project_id=project_id,
        time_range=time_range,
    )