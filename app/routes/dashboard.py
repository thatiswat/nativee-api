from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.customer_dashboard import DashboardResponse
from app.services.customer_dashboard_service import (
    CustomerDashboardService,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Customer Dashboard",
)
def dashboard(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return CustomerDashboardService(db).overview(
        current_user,
    )