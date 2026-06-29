from pydantic import BaseModel


class CreateAPIKeyRequest(BaseModel):
    name: str
    live: bool = True
    plan_id: int = 1  # defaults to Free plan


class CreateAPIKeyResponse(BaseModel):
    id: int
    name: str
    api_key: str