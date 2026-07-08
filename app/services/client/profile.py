from app.schemas.client.profile import (
    ClientProfileResponse,
)

from app.schemas.shared.identity import (
    IdentityClaims,
)


class ClientProfileService:

    def profile(
        self,
        user: IdentityClaims,
    ) -> ClientProfileResponse:

        return ClientProfileResponse(
            id=user.public_id,
            email=user.email,
            name=user.name,
            avatar=None,
            primary_language=None,
        )