from sqlalchemy.orm import Session

from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.usage_repository import UsageRepository

from app.schemas.project_dashboard import (
    DashboardAPIKey,
    DashboardLimits,
    DashboardPerformance,
    DashboardPlan,
    DashboardProject,
    DashboardResponse,
    DashboardTimeRange,
    DashboardUsage,
)

from app.models.user import User


class ProjectDashboardService:
    """
    Project dashboard service.

    - JWT user authentication
    - project-scoped analytics
    - optional API key reporting dimension
    - time-range aware metrics
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.project_repository = ProjectRepository(db)
        self.api_key_repository = APIKeyRepository(db)
        self.usage_repository = UsageRepository(db)

    def overview(
        self,
        user: User,
        project_id: int,
        time_range: DashboardTimeRange = DashboardTimeRange.LAST_24_HOURS,
    ) -> DashboardResponse:

        # -----------------------------
        # 1. Validate project ownership
        # -----------------------------
        project = self.project_repository.get_owned(
            owner_id=user.id,
            project_id=project_id,
        )

        if project is None:
            raise PermissionError(
                "You do not have access to this project"
            )

        # -----------------------------
        # 2. Optional API key (reporting only)
        # -----------------------------
        api_key = (
            project.api_keys[0]
            if project.api_keys
            else None
        )

        plan = api_key.plan if api_key else None

        # -----------------------------
        # 3. Usage metrics
        # -----------------------------
        total_requests = self.usage_repository.get_total_requests(
            project_id,
        )

        requests_today = self.usage_repository.get_requests_today(
            project_id,
        )

        average_latency = self.usage_repository.get_average_latency(
            project_id,
        )

        success_rate = self.usage_repository.get_success_rate(
            project_id,
        )

        # -----------------------------
        # 4. Response assembly
        # -----------------------------
        return DashboardResponse(
            project=DashboardProject(
                id=project.id,
                name=project.name,
            ),
            api_key=DashboardAPIKey(
                id=api_key.id,
                name=api_key.name,
            ) if api_key else None,
            plan=DashboardPlan(
                id=plan.id,
                name=plan.name,
            ) if plan else None,
            usage=DashboardUsage(
                total_requests=total_requests,
                requests_today=requests_today,
            ),
            limits=DashboardLimits(
                requests_per_minute=plan.requests_per_minute if plan else 0,
                requests_per_month=plan.requests_per_month if plan else 0,
            ),
            performance=DashboardPerformance(
                average_latency_ms=average_latency,
                success_rate=success_rate,
            ),
        )