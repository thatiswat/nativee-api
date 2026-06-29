from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)

    return service.overview(
        request.state.api_key,
    )