from pydantic import BaseModel


class DashboardUser(BaseModel):
    id: int
    name: str


class DashboardStats(BaseModel):
    projects: int
    api_keys: int
    requests: int
    current_plan: str


class DashboardProject(BaseModel):
    id: int
    name: str
    plan: str
    api_keys: int
    requests: int


class DashboardActivity(BaseModel):
    id: int
    message: str
    created_at: str


class DashboardResponse(BaseModel):
    user: DashboardUser
    stats: DashboardStats
    projects: list[DashboardProject]
    activities: list[DashboardActivity]