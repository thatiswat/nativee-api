from pydantic import BaseModel


class DashboardProject(BaseModel):
    id: int
    name: str


class DashboardAPIKey(BaseModel):
    id: int
    name: str


class DashboardPlan(BaseModel):
    id: int
    name: str


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
    project: DashboardProject
    api_key: DashboardAPIKey
    plan: DashboardPlan
    usage: DashboardUsage
    limits: DashboardLimits
    performance: DashboardPerformance