from fastapi import APIRouter
from fastapi import Request

from app.schemas.error import ErrorResponse
from app.schemas.me import MeResponse
from app.services.identity_service import IdentityService

router = APIRouter(
    prefix="/me",
    tags=["Identity"],
)

service = IdentityService()


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
def get_me(
    request: Request,
):
    """
    Returns information about the authenticated API key,
    including its assigned subscription plan.
    """

    return service.get_me(
        request.state.api_key,
    )