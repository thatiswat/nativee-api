from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.models.usage_log import UsageLog


class AnalyticsRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def total_requests(
        self,
        project_id: int,
    ):
        return (
            self.db.query(func.count(UsageLog.id))
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
            )
            .scalar()
        )

    def average_latency(
        self,
        project_id: int,
    ):
        average = (
            self.db.query(
                func.avg(UsageLog.latency_ms),
            )
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
            )
            .scalar()
        )

        return float(average or 0.0)

    def success_rate(
        self,
        project_id: int,
    ):
        total = (
            self.db.query(func.count(UsageLog.id))
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
            )
            .scalar()
        )

        success = (
            self.db.query(func.count(UsageLog.id))
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
                UsageLog.success.is_(True),
            )
            .scalar()
        )

        if total == 0:
            return 0

        return round(success * 100 / total, 2)

    def requests_per_day(
        self,
        project_id: int,
    ):
        return (
            self.db.query(
                cast(UsageLog.created_at, Date).label("day"),
                func.count(UsageLog.id).label("requests"),
            )
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
            )
            .group_by(
                cast(UsageLog.created_at, Date),
            )
            .order_by(
                cast(UsageLog.created_at, Date),
            )
            .all()
        )

    def provider_breakdown(
        self,
        project_id: int,
    ):
        return (
            self.db.query(
                UsageLog.provider,
                func.count(UsageLog.id),
            )
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
            )
            .group_by(
                UsageLog.provider,
            )
            .all()
        )

    def endpoint_breakdown(
        self,
        project_id: int,
    ):
        return (
            self.db.query(
                UsageLog.endpoint,
                func.count(UsageLog.id),
            )
            .join(
                APIKey,
                UsageLog.api_key_id == APIKey.id,
            )
            .filter(
                APIKey.project_id == project_id,
            )
            .group_by(
                UsageLog.endpoint,
            )
            .all()
        )