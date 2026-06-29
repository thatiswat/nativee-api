from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self, db):
        self.repository = AnalyticsRepository(db)

    def overview(self):

        return {
            "total_requests": self.repository.total_requests(),
            "average_latency": self.repository.average_latency(),
            "success_rate": self.repository.success_rate(),
        }