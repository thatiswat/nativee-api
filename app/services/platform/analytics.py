from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self, db):
        self.repository = AnalyticsRepository(db)

    def overview(
        self,
        project_id: int,
    ):

        return {
            "total_requests": self.repository.total_requests(project_id),
            "average_latency": self.repository.average_latency(project_id),
            "success_rate": self.repository.success_rate(project_id),
            "requests_per_day": self.repository.requests_per_day(project_id),
            "provider_breakdown": self.repository.provider_breakdown(project_id),
            "endpoint_breakdown": self.repository.endpoint_breakdown(project_id),
        }