from app.schemas.me import (
    APIKeyInfo,
    MeResponse,
    PlanInfo,
    ProjectInfo,
)


class IdentityService:
    """
    Uses the authenticated API Key provided by the API Key dependency.
    """

    def get_me(
        self,
        api_key,
    ) -> MeResponse:

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