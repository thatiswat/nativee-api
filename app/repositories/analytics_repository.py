from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.usage_log import UsageLog


class AnalyticsRepository:

    def __init__(self, db: Session):
        self.db = db

    def total_requests(self):

        return (
            self.db.query(func.count(UsageLog.id))
            .scalar()
        )

    def average_latency(self):

        return (
            self.db.query(func.avg(UsageLog.latency_ms))
            .scalar()
        )

    def success_rate(self):

        total = (
            self.db.query(func.count(UsageLog.id))
            .scalar()
        )

        success = (
            self.db.query(func.count(UsageLog.id))
            .filter(UsageLog.success == True)
            .scalar()
        )

        if total == 0:
            return 0

        return round(success * 100 / total, 2)