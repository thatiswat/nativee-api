from sqlalchemy.orm import Session

from app.schemas.dashboard import (
    DashboardIdentity,
    DashboardLimits,
    DashboardPerformance,
    DashboardResponse,
    DashboardUsage,
)
from app.services.usage_service import UsageService


class DashboardService:
    """
    Developer dashboard.

    Composes existing platform services instead of
    querying repositories directly.
    """

    def __init__(self, db: Session):
        self.usage_service = UsageService(db)

    def overview(
        self,
        api_key,
    ) -> DashboardResponse:

        return DashboardResponse(
            identity=DashboardIdentity(
                api_key=api_key.name,
                plan=api_key.plan.name,
            ),
            usage=DashboardUsage(
                total_requests=self.usage_service.get_total_requests(
                    api_key.id
                ),
                requests_today=self.usage_service.get_requests_today(
                    api_key.id
                ),
            ),
            limits=DashboardLimits(
                requests_per_minute=api_key.plan.requests_per_minute,
                requests_per_month=api_key.plan.requests_per_month,
            ),
            performance=DashboardPerformance(
                average_latency_ms=self.usage_service.get_average_latency(
                    api_key.id
                ),
                success_rate=self.usage_service.get_success_rate(
                    api_key.id
                ),
            ),
        )