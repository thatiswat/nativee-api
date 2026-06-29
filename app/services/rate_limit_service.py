from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.usage_log import UsageLog


class RateLimitService:

    def __init__(self, db: Session):
        self.db = db

    def is_allowed(
        self,
        api_key_id: int,
        limit: int = 10,
    ) -> bool:

        one_minute_ago = (
            datetime.utcnow()
            - timedelta(minutes=1)
        )

        requests = (
            self.db.query(UsageLog)
            .filter(
                UsageLog.api_key_id == api_key_id,
                UsageLog.created_at >= one_minute_ago,
            )
            .count()
        )

        return requests < limit