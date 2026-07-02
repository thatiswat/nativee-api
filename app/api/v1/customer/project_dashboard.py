from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.api_key import require_api_key
from app.models.api_key import APIKey
from app.schemas.project_dashboard import DashboardResponse
from app.schemas.error import ErrorResponse
from app.services.project_dashboard_service import (
    ProjectDashboardService,
)

router = APIRouter(
    prefix="/project-dashboard",
    tags=["Project Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Project Dashboard",
    description="""
Returns usage statistics for the authenticated API Key.

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
            "description": "API key disabled",
        },
        429: {
            "model": ErrorResponse,
            "description": "Rate limit or monthly quota exceeded",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def get_dashboard(
    api_key: APIKey = Depends(require_api_key),
    db: Session = Depends(get_db),
):
    return ProjectDashboardService(db).overview(
        api_key,
    )