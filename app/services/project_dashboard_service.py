from sqlalchemy.orm import Session

from app.schemas.project_dashboard import (
    DashboardAPIKey,
    DashboardLimits,
    DashboardPerformance,
    DashboardPlan,
    DashboardProject,
    DashboardResponse,
    DashboardUsage,
    DashboardTimeRange,
)

from app.services.usage_service import UsageService
from app.models.user import User
from app.models.project import Project
from app.models.api_key import APIKey


class ProjectDashboardService:
    """
    Project dashboard service.

    - JWT user authentication
    - project-scoped analytics
    - optional API key reporting dimension
    - time-range aware metrics
    """

    def __init__(self, db: Session):
        self.db = db
        self.usage_service = UsageService(db)

    def overview(
        self,
        user: User,
        project_id: int,
        time_range: DashboardTimeRange = DashboardTimeRange.LAST_24_HOURS,
    ) -> DashboardResponse:

        # -----------------------------
        # 1. Validate project ownership
        # -----------------------------
        project = (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if not project or project.owner_id != user.id:
            raise PermissionError("You do not have access to this project")

        # -----------------------------
        # 2. Optional API key (reporting only)
        # -----------------------------
        api_key = (
            self.db.query(APIKey)
            .filter(APIKey.project_id == project_id)
            .first()
        )

        plan = api_key.plan if api_key else None

        # -----------------------------
        # 3. Usage metrics (time-aware, project scoped)
        # -----------------------------
        total_requests = self.usage_service.get_total_requests(
            project_id=project_id,
            time_range=time_range,
        )

        requests_today = self.usage_service.get_requests_today(
            project_id=project_id,
        )

        average_latency = self.usage_service.get_average_latency(
            project_id=project_id,
            time_range=time_range,
        )

        success_rate = self.usage_service.get_success_rate(
            project_id=project_id,
            time_range=time_range,
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