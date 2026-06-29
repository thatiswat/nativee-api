from sqlalchemy.orm import Session

from app.models.usage_log import UsageLog


class UsageRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        usage: UsageLog,
    ):
        self.db.add(usage)
        self.db.commit()
        self.db.refresh(usage)

        return usage