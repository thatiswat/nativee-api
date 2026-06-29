from fastapi import APIRouter
from fastapi import Request

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
)
def get_me(
    request: Request,
):
    """
    Returns the authenticated API Key and Plan.
    """

    return service.get_me(
        request.state.api_key,
    )