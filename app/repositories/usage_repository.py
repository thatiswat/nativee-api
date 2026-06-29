from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.usage_log import UsageLog


class UsageRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create(
        self,
        usage: UsageLog,
    ) -> UsageLog:
        self.db.add(usage)
        self.db.commit()
        self.db.refresh(usage)

        return usage

    # --------------------------------------------------
    # Read
    # --------------------------------------------------

    def get_total_requests(
        self,
        api_key_id: int,
    ) -> int:
        return (
            self.db.query(UsageLog)
            .filter(
                UsageLog.api_key_id == api_key_id,
            )
            .count()
        )

    def get_requests_today(
        self,
        api_key_id: int,
    ) -> int:
        today = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        return (
            self.db.query(UsageLog)
            .filter(
                UsageLog.api_key_id == api_key_id,
                UsageLog.created_at >= today,
            )
            .count()
        )

    def get_average_latency(
        self,
        api_key_id: int,
    ) -> float:
        average = (
            self.db.query(
                func.avg(UsageLog.latency_ms),
            )
            .filter(
                UsageLog.api_key_id == api_key_id,
            )
            .scalar()
        )

        return float(average or 0.0)

    def get_success_rate(
        self,
        api_key_id: int,
    ) -> float:
        total = (
            self.db.query(UsageLog)
            .filter(
                UsageLog.api_key_id == api_key_id,
            )
            .count()
        )

        if total == 0:
            return 0.0

        successful = (
            self.db.query(UsageLog)
            .filter(
                UsageLog.api_key_id == api_key_id,
                UsageLog.success.is_(True),
            )
            .count()
        )

        return (successful / total) * 100