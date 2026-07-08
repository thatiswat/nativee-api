from fastapi import APIRouter, Depends

from app.dependencies.auth import (
    get_current_user,
)

from app.schemas.shared.identity import (
    IdentityClaims,
)

from app.services.client.profile import (
    ClientProfileService,
)

router = APIRouter(
    prefix="/profile",
    tags=["Client"],
)


@router.get("")
async def profile(
    user: IdentityClaims = Depends(
        get_current_user,
    ),
):
    service = ClientProfileService()

    return {
        "success": True,
        "profile": service.profile(
            user,
        ),
    }