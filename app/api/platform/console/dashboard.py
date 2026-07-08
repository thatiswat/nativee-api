from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.schemas.shared.identity import (
    IdentityClaims,
)

from app.schemas.platform.dashboard import (
    DeveloperDashboardResponse,
)

from app.services.platform.customer_dashboard import (
    CustomerDashboardService,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DeveloperDashboardResponse,
    summary="Customer Dashboard",
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: IdentityClaims = Depends(
        get_current_user,
    ),
):
    service = CustomerDashboardService(
        db,
    )

    return service.overview(
        current_user,
    )