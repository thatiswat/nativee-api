from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.dashboard import DashboardResponse
from app.schemas.error import ErrorResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Usage Summary",
    description="""
Returns usage statistics for the authenticated API Key.

Includes:

- Total requests
- Requests today
- Requests this month
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
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Returns usage statistics for the authenticated API key.
    """

    service = DashboardService(db)

    return service.overview(
        request.state.api_key,
    )