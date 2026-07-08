from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.platform.error import ErrorResponse
from app.schemas.platform.plan import PlansResponse
from app.services.platform.plans import PlanService

router = APIRouter(
    prefix="/plans",
)


@router.get(
    "",
    response_model=PlansResponse,
    summary="Available Plans",
    description="""
Returns all publicly available Nativeee platform plans.

Useful for pricing pages,
developer onboarding,
and plan comparisons.
""",
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def get_plans(
    db: Session = Depends(get_db),
):
    """
    Returns all available subscription plans.
    """

    service = PlanService(db)

    plans = service.get_all()

    return PlansResponse(
        success=True,
        plans=[
            {
                "id": plan.id,
                "name": plan.name,
                "requests_per_minute": plan.requests_per_minute,
                "requests_per_month": plan.requests_per_month,
            }
            for plan in plans
        ],
    )