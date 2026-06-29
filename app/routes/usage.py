from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.usage_service import UsageService
from app.schemas.usage import UsageSummaryResponse


router = APIRouter(
    prefix="/usage",
    tags=["Usage"],
)


@router.get(
    "",
    response_model=UsageSummaryResponse,  # ✅ ADDED: API contract enforcement
)
def get_usage(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Returns usage summary for the authenticated API key.
    """

    service = UsageService(db)

    return service.get_usage_summary(
        request.state.api_key
    )