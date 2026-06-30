from pydantic import BaseModel


class ProjectInfo(BaseModel):
    id: int
    name: str


class APIKeyInfo(BaseModel):
    id: int
    name: str


class PlanInfo(BaseModel):
    id: int
    name: str
    requests_per_minute: int
    requests_per_month: int


class MeResponse(BaseModel):
    project: ProjectInfo
    api_key: APIKeyInfo
    plan: PlanInfo