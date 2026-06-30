from app.repositories.usage_repository import UsageRepository


class QuotaService:
    """
    Enforces monthly plan quotas.

    Example:

    Free Plan
        3,000 requests/month

    Growth Plan
        1,000,000 requests/month
    """

    def __init__(self, db):
        self.repository = UsageRepository(db)

    def is_allowed(
        self,
        api_key,
    ) -> dict:
        """
        Check whether the API key has remaining
        monthly quota.
        """

        used = self.repository.get_requests_this_month(
            api_key.id,
        )

        limit = api_key.plan.requests_per_month

        remaining = max(
            0,
            limit - used,
        )

        return {
            "allowed": used < limit,
            "used": used,
            "remaining": remaining,
            "limit": limit,
        }