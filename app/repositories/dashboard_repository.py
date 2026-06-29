from sqlalchemy.orm import Session


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def requests_today(self):
        ...

    def requests_this_month(self):
        ...

    def average_latency(self):
        ...

    def success_rate(self):
        ...

    def active_api_keys(self):
        ...

    def top_provider(self):
        ...

    def top_endpoint(self):
        ...