from sqlalchemy.orm import Session

from app.core.request_context import RequestContext
from app.models.usage_log import UsageLog
from app.repositories.usage_repository import UsageRepository


class UsageService:
    """
    Handles all platform usage logging.

    Every API request that reaches the platform should
    eventually create one UsageLog record.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = UsageRepository(db)

    def log(
        self,
        context: RequestContext,
    ) -> UsageLog:
        """
        Persist a usage log from the current request context.
        """

        usage = UsageLog(
            api_key_id=context.api_key_id,
            endpoint=context.endpoint,
            provider=context.provider,
            latency_ms=context.latency_ms,
            success=context.success,
        )

        return self.repository.create(usage)