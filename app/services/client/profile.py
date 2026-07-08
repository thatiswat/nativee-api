from app.schemas.client.profile import (
    ClientProfileResponse,
)


class ClientProfileService:

    def profile(
        self,
        user: dict,
    ) -> ClientProfileResponse:

        return ClientProfileResponse(
            id=user["sub"],
            email=user.get("email"),
            name=user.get("user_metadata", {}).get("name"),
            avatar=user.get("user_metadata", {}).get("avatar_url"),
            primary_language=user.get(
                "user_metadata",
                {},
            ).get("primary_language"),
        )