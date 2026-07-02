from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.api_key import require_api_key
from app.schemas.usage import UsageSummaryResponse
from app.services.usage_service import UsageService

router = APIRouter(
    prefix="/usage",
    tags=["Usage"],
)


@router.get(
    "",
    response_model=UsageSummaryResponse,
    summary="Usage Summary",
)
def usage(
    api_key=Depends(require_api_key),
    db: Session = Depends(get_db),
):
    """
    Returns usage summary for the authenticated API key.
    """

    service = UsageService(db)

    return service.get_usage_summary(
        api_key,
    )