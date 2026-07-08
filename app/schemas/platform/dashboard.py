from enum import Enum
from typing import Optional

from pydantic import BaseModel


# ==========================================================
# Common
# ==========================================================

class DashboardTimeRange(str, Enum):
    LAST_24_HOURS = "24h"
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"


# ==========================================================
# Developer Dashboard
# ==========================================================

class DashboardUser(BaseModel):
    id: int
    name: str


class DashboardStats(BaseModel):
    projects: int
    api_keys: int
    requests: int
    current_plan: str


class DashboardProjectSummary(BaseModel):
    id: int
    name: str
    plan: str
    api_keys: int
    requests: int


class DashboardActivity(BaseModel):
    id: int
    message: str
    created_at: str


class DeveloperDashboardResponse(BaseModel):
    user: DashboardUser
    stats: DashboardStats
    projects: list[DashboardProjectSummary]
    activities: list[DashboardActivity]


# ==========================================================
# Project Dashboard
# ==========================================================

class ProjectInfo(BaseModel):
    id: int
    name: str


class APIKeyInfo(BaseModel):
    id: int
    name: Optional[str] = None


class PlanInfo(BaseModel):
    id: int
    name: str


class UsageInfo(BaseModel):
    total_requests: int
    requests_today: int


class LimitsInfo(BaseModel):
    requests_per_minute: int
    requests_per_month: int


class PerformanceInfo(BaseModel):
    average_latency_ms: float
    success_rate: float


class ProjectDashboardResponse(BaseModel):
    project: ProjectInfo
    api_key: Optional[APIKeyInfo] = None
    plan: Optional[PlanInfo] = None
    usage: UsageInfo
    limits: LimitsInfo
    performance: PerformanceInfo