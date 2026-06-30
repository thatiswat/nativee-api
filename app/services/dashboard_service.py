from sqlalchemy.orm import Session

from app.schemas.dashboard import (
    DashboardAPIKey,
    DashboardLimits,
    DashboardPerformance,
    DashboardPlan,
    DashboardProject,
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

        plan = api_key.plan
        project = api_key.project

        total_requests = self.usage_service.get_total_requests(
            api_key.id
        )

        requests_today = self.usage_service.get_requests_today(
            api_key.id
        )

        average_latency = self.usage_service.get_average_latency(
            api_key.id
        )

        success_rate = self.usage_service.get_success_rate(
            api_key.id
        )

        return DashboardResponse(
            project=DashboardProject(
                id=project.id,
                name=project.name,
            ),
            api_key=DashboardAPIKey(
                id=api_key.id,
                name=api_key.name,
            ),
            plan=DashboardPlan(
                id=plan.id,
                name=plan.name,
            ),
            usage=DashboardUsage(
                total_requests=total_requests,
                requests_today=requests_today,
            ),
            limits=DashboardLimits(
                requests_per_minute=plan.requests_per_minute,
                requests_per_month=plan.requests_per_month,
            ),
            performance=DashboardPerformance(
                average_latency_ms=average_latency,
                success_rate=success_rate,
            ),
        )