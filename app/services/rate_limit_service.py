from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.models.usage_log import UsageLog


class RateLimitService:

    def __init__(self, db: Session):
        self.db = db

    def is_allowed(
        self,
        api_key: APIKey,
    ) -> dict:
        """
        Check whether an API key is within its
        requests-per-minute limit.
        """

        limit = api_key.plan.requests_per_minute

        one_minute_ago = (
            datetime.utcnow()
            - timedelta(minutes=1)
        )

        requests = (
            self.db.query(UsageLog)
            .filter(
                UsageLog.api_key_id == api_key.id,
                UsageLog.created_at >= one_minute_ago,
            )
            .count()
        )

        remaining = max(
            0,
            limit - requests,
        )

        return {
            "allowed": requests < limit,
            "remaining": remaining,
            "limit": limit,
        }