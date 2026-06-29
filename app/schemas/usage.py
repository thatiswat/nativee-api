from pydantic import BaseModel


class UsageSummaryResponse(BaseModel):
    api_key: str
    plan: str

    total_requests: int
    requests_today: int

    average_latency_ms: float
    success_rate: float