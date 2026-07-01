from enum import Enum
from typing import Optional
from pydantic import BaseModel


class DashboardTimeRange(str, Enum):
    LAST_24_HOURS = "24h"
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"


class DashboardProject(BaseModel):
    id: int
    name: str


class DashboardAPIKey(BaseModel):
    id: int
    name: Optional[str] = None


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
    api_key: Optional[DashboardAPIKey] = None
    plan: Optional[DashboardPlan] = None
    usage: DashboardUsage
    limits: DashboardLimits
    performance: DashboardPerformance