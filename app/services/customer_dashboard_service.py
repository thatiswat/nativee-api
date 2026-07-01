from sqlalchemy.orm import Session

from app.schemas.customer_dashboard import (
    DashboardActivity,
    DashboardProject,
    DashboardResponse,
    DashboardStats,
    DashboardUser,
)


class CustomerDashboardService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def overview(
        self,
        user,
    ) -> DashboardResponse:

        return DashboardResponse(
            user=DashboardUser(
                id=user.id,
                name=user.name,
            ),
            stats=DashboardStats(
                projects=0,
                api_keys=0,
                requests=0,
                current_plan="Free",
            ),
            projects=[],
            activities=[],
        )