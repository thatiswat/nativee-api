from sqlalchemy.orm import Session

from app.models.plan import Plan


class PlanRepository:

    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(self, plan: Plan) -> Plan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)

        return plan

    # ----------------------------------
    # Read
    # ----------------------------------

    def get(self, plan_id: int) -> Plan | None:
        return (
            self.db.query(Plan)
            .filter(Plan.id == plan_id)
            .first()
        )

    def get_by_name(self, name: str) -> Plan | None:
        return (
            self.db.query(Plan)
            .filter(Plan.name == name)
            .first()
        )

    def get_all(self) -> list[Plan]:
        return (
            self.db.query(Plan)
            .filter(Plan.active == True)
            .order_by(Plan.id.asc())
            .all()
        )

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(self, plan: Plan) -> Plan:
        self.db.commit()
        self.db.refresh(plan)

        return plan

    # ----------------------------------
    # Delete (Soft Delete)
    # ----------------------------------

    def deactivate(self, plan: Plan) -> Plan:
        plan.active = False

        self.db.commit()
        self.db.refresh(plan)

        return plan