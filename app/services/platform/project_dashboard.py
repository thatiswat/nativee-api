from sqlalchemy.orm import Session

from app.schemas.shared.identity import IdentityClaims
from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.usage_repository import UsageRepository

from app.schemas.platform.dashboard import (
    DashboardTimeRange,
    ProjectDashboardResponse,
    ProjectInfo,
    APIKeyInfo,
    PlanInfo,
    UsageInfo,
    LimitsInfo,
    PerformanceInfo,
)


class ProjectDashboardService:
    """
    Project dashboard service.

    - JWT user authentication
    - Project-scoped analytics
    - Optional API key reporting
    - Time-range aware metrics
    """

    def __init__(self, db: Session):
        self.db = db

        self.project_repository = ProjectRepository(db)
        self.api_key_repository = APIKeyRepository(db)
        self.usage_repository = UsageRepository(db)

    def overview(
        self,
        user: IdentityClaims,
        project_id: int,
        time_range: DashboardTimeRange = DashboardTimeRange.LAST_24_HOURS,
    ) -> ProjectDashboardResponse:

        # ----------------------------------
        # Validate project ownership
        # ----------------------------------
        project = self.project_repository.get_owned(
            owner_id=user.id,
            project_id=project_id,
        )

        if project is None:
            raise PermissionError(
                "You do not have access to this project"
            )

        # ----------------------------------
        # Optional API Key
        # ----------------------------------
        api_key = (
            project.api_keys[0]
            if project.api_keys
            else None
        )

        plan = api_key.plan if api_key else None

        # ----------------------------------
        # Usage metrics
        # ----------------------------------
        total_requests = self.usage_repository.get_total_requests(
            project.id,
        )

        requests_today = self.usage_repository.get_requests_today(
            project.id,
        )

        average_latency = self.usage_repository.get_average_latency(
            project.id,
        )

        success_rate = self.usage_repository.get_success_rate(
            project.id,
        )

        # ----------------------------------
        # Response
        # ----------------------------------
        return ProjectDashboardResponse(
            project=ProjectInfo(
                id=project.id,
                name=project.name,
            ),
            api_key=APIKeyInfo(
                id=api_key.id,
                name=api_key.name,
            ) if api_key else None,
            plan=PlanInfo(
                id=plan.id,
                name=plan.name,
            ) if plan else None,
            usage=UsageInfo(
                total_requests=total_requests,
                requests_today=requests_today,
            ),
            limits=LimitsInfo(
                requests_per_minute=plan.requests_per_minute if plan else 0,
                requests_per_month=plan.requests_per_month if plan else 0,
            ),
            performance=PerformanceInfo(
                average_latency_ms=average_latency,
                success_rate=success_rate,
            ),
        )