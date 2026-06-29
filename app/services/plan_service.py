from sqlalchemy.orm import Session

from app.models.plan import Plan
from app.repositories.plan_repository import PlanRepository


class PlanService:

    def __init__(self, db: Session):
        self.repository = PlanRepository(db)

    # ----------------------------------
    # Default Platform Plans
    # ----------------------------------

    def seed_defaults(self):

        plans = [
            {
                "name": "Free",
                "requests_per_minute": 10,
                "requests_per_month": 3000,
            },
            {
                "name": "Starter",
                "requests_per_minute": 60,
                "requests_per_month": 100000,
            },
            {
                "name": "Growth",
                "requests_per_minute": 250,
                "requests_per_month": 1000000,
            },
            {
                "name": "Enterprise",
                "requests_per_minute": 1000,
                "requests_per_month": 10000000,
            },
        ]

        for item in plans:

            exists = self.repository.get_by_name(
                item["name"]
            )

            if exists:
                continue

            self.repository.create(
                Plan(**item)
            )

    # ----------------------------------
    # Read
    # ----------------------------------

    def get_all(self):
        return self.repository.get_all()

    def get(self, plan_id: int):
        return self.repository.get(plan_id)