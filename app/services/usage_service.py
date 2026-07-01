from sqlalchemy.orm import Session

from app.models.usage_log import UsageLog
from app.repositories.usage_repository import UsageRepository
from app.schemas.usage import UsageSummaryResponse


class UsageService:
    """
    Handles all platform usage logging and metrics.

    Now PROJECT-SCOPED (not API-key scoped).
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = UsageRepository(db)

    # --------------------------------------------------
    # Write path
    # --------------------------------------------------
    def log(self, context) -> UsageLog:
        """
        context must contain:
        - project_id
        - endpoint
        - provider
        - latency_ms
        - success
        """

        usage = UsageLog(
            project_id=context.project_id,
            endpoint=context.endpoint,
            provider=context.provider,
            latency_ms=context.latency_ms,
            success=context.success,
        )

        return self.repository.create(usage)

    # --------------------------------------------------
    # Read paths (PROJECT scoped)
    # --------------------------------------------------
    def get_total_requests(self, project_id: int) -> int:
        return self.repository.get_total_requests(project_id)

    def get_requests_today(self, project_id: int) -> int:
        return self.repository.get_requests_today(project_id)

    def get_average_latency(self, project_id: int) -> float:
        return self.repository.get_average_latency(project_id)

    def get_success_rate(self, project_id: int) -> float:
        return self.repository.get_success_rate(project_id)

    # --------------------------------------------------
    # Business layer (dashboard contract)
    # --------------------------------------------------
    def get_usage_summary(self, project, plan) -> UsageSummaryResponse:
        return UsageSummaryResponse(
            project=project.name,
            plan=plan.name if plan else None,
            total_requests=self.get_total_requests(project.id),
            requests_today=self.get_requests_today(project.id),
            average_latency_ms=self.get_average_latency(project.id),
            success_rate=self.get_success_rate(project.id),
        )