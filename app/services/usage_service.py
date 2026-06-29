from sqlalchemy.orm import Session

from app.core.request_context import RequestContext
from app.models.usage_log import UsageLog
from app.repositories.usage_repository import UsageRepository
from app.schemas.usage import UsageSummaryResponse


class UsageService:
    """
    Handles all platform usage logging and metrics.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = UsageRepository(db)

    # --------------------------------------------------
    # Write path
    # --------------------------------------------------
    def log(
        self,
        context: RequestContext,
    ) -> UsageLog:

        usage = UsageLog(
            api_key_id=context.api_key_id,
            endpoint=context.endpoint,
            provider=context.provider,
            latency_ms=context.latency_ms,
            success=context.success,
        )

        return self.repository.create(usage)

    # --------------------------------------------------
    # Read paths
    # --------------------------------------------------
    def get_total_requests(self, api_key_id: int) -> int:
        return self.repository.get_total_requests(api_key_id)

    def get_requests_today(self, api_key_id: int) -> int:
        return self.repository.get_requests_today(api_key_id)

    def get_average_latency(self, api_key_id: int) -> float:
        return self.repository.get_average_latency(api_key_id)

    def get_success_rate(self, api_key_id: int) -> float:
        return self.repository.get_success_rate(api_key_id)

    # --------------------------------------------------
    # Business layer (platform contract)
    # --------------------------------------------------
    def get_usage_summary(
        self,
        api_key,
    ) -> UsageSummaryResponse:

        return UsageSummaryResponse(
            api_key=api_key.name,
            plan=api_key.plan.name,
            total_requests=self.get_total_requests(api_key.id),
            requests_today=self.get_requests_today(api_key.id),
            average_latency_ms=self.get_average_latency(api_key.id),
            success_rate=self.get_success_rate(api_key.id),
        )