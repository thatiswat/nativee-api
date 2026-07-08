from fastapi import APIRouter, Depends

from app.dependencies.supabase import (
    get_current_client,
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
    user=Depends(
        get_current_client,
    ),
):

    service = ClientProfileService()

    return {
        "success": True,
        "profile": service.profile(
            user,
        ),
    }