from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.models.project import Project
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
        project_id: int,
    ) -> int:
        return (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
            )
            .count()
        )

    def count_by_user(
        self,
        owner_id: int,
    ) -> int:
        return (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .join(Project, APIKey.project_id == Project.id)
            .filter(
                Project.owner_id == owner_id,
            )
            .count()
        )

    def count_by_project(
        self,
        project_id: int,
    ) -> int:
        return (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
            )
            .count()
        )

    def get_requests_today(
        self,
        project_id: int,
    ) -> int:
        today = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        return (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
                UsageLog.created_at >= today,
            )
            .count()
        )

    def get_requests_this_month(
        self,
        project_id: int,
    ) -> int:
        """
        Returns total requests made this month.
        """

        start_of_month = datetime.utcnow().replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        return (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
                UsageLog.created_at >= start_of_month,
            )
            .count()
        )

    def get_average_latency(
        self,
        project_id: int,
    ) -> float:
        average = (
            self.db.query(
                func.avg(UsageLog.latency_ms),
            )
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
            )
            .scalar()
        )

        return float(average or 0.0)

    def get_success_rate(
        self,
        project_id: int,
    ) -> float:
        total = (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
            )
            .count()
        )

        if total == 0:
            return 0.0

        successful = (
            self.db.query(UsageLog)
            .join(APIKey, UsageLog.api_key_id == APIKey.id)
            .filter(
                APIKey.project_id == project_id,
                UsageLog.success.is_(True),
            )
            .count()
        )

        return (successful / total) * 100