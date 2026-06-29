from app.schemas.me import (
    APIKeyResponse,
    MeResponse,
    PlanResponse,
)


class IdentityService:
    """
    Handles authenticated identity.

    Uses the API key already loaded by AuthenticationMiddleware.
    No database queries are required.
    """

    def get_me(
        self,
        api_key,
    ) -> MeResponse:

        return MeResponse(
            api_key=APIKeyResponse(
                id=api_key.id,
                name=api_key.name,
            ),
            plan=PlanResponse(
                id=api_key.plan.id,
                name=api_key.plan.name,
                requests_per_minute=api_key.plan.requests_per_minute,
                requests_per_month=api_key.plan.requests_per_month,
            ),
        )