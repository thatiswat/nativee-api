from pydantic import BaseModel, ConfigDict


class PlanResponse(BaseModel):
    id: int
    name: str
    requests_per_minute: int
    requests_per_month: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Free",
                "requests_per_minute": 60,
                "requests_per_month": 10000,
            }
        }
    )


class PlansResponse(BaseModel):
    success: bool
    plans: list[PlanResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "plans": [
                    {
                        "id": 1,
                        "name": "Free",
                        "requests_per_minute": 60,
                        "requests_per_month": 10000,
                    },
                    {
                        "id": 2,
                        "name": "Pro",
                        "requests_per_minute": 300,
                        "requests_per_month": 100000,
                    },
                ],
            }
        }
    )