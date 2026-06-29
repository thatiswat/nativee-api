from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.plan_service import PlanService

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.get("")
def get_plans(
    db: Session = Depends(get_db),
):
    service = PlanService(db)

    plans = service.get_all()

    return {
        "success": True,
        "plans": [
            {
                "id": plan.id,
                "name": plan.name,
                "requests_per_minute": plan.requests_per_minute,
                "requests_per_month": plan.requests_per_month,
            }
            for plan in plans
        ],
    }