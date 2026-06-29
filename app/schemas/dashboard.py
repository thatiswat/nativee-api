from pydantic import BaseModel


class DashboardIdentity(BaseModel):
    api_key: str
    plan: str


class DashboardUsage(BaseModel):
    total_requests: int
    requests_today: int


class DashboardLimits(BaseModel):
    requests_per_minute: int
    requests_per_month: int


class DashboardPerformance(BaseModel):
    average_latency_ms: float
    success_rate: float


class DashboardResponse(BaseModel):
    identity: DashboardIdentity
    usage: DashboardUsage
    limits: DashboardLimits
    performance: DashboardPerformance