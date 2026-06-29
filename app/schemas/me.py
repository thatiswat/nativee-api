from pydantic import BaseModel


class PlanResponse(BaseModel):
    id: int
    name: str
    requests_per_minute: int
    requests_per_month: int


class APIKeyResponse(BaseModel):
    id: int
    name: str


class MeResponse(BaseModel):
    api_key: APIKeyResponse
    plan: PlanResponse