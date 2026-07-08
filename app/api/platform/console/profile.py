from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies.api_key import (
    require_api_key,
)

from app.schemas.platform.error import (
    ErrorResponse,
)

from app.schemas.platform.identity import (
    APIKeyInfo,
    MeResponse,
    PlanInfo,
    ProjectInfo,
)


router = APIRouter(
    prefix="/me",
    tags=["Identity"],
)


@router.get(
    "",
    response_model=MeResponse,
    summary="Authenticated Identity",
    description="""
Returns the authenticated API Key
and the assigned subscription plan.
""",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        },
        403: {
            "model": ErrorResponse,
            "description": "API key disabled",
        },
        429: {
            "model": ErrorResponse,
            "description": "Rate limit or monthly quota exceeded",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def me(
    api_key=Depends(require_api_key),
):
    """
    Returns information about the authenticated API key,
    including its assigned project and subscription plan.
    """

    return MeResponse(
        project=ProjectInfo(
            id=api_key.project.id,
            name=api_key.project.name,
        ),
        api_key=APIKeyInfo(
            id=api_key.id,
            name=api_key.name,
        ),
        plan=PlanInfo(
            id=api_key.plan.id,
            name=api_key.plan.name,
            requests_per_minute=api_key.plan.requests_per_minute,
            requests_per_month=api_key.plan.requests_per_month,
        ),
    )