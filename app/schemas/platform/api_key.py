from pydantic import BaseModel
from pydantic import ConfigDict


class CreateAPIKeyRequest(BaseModel):
    name: str
    live: bool = True

    project_id: int = 1
    plan_id: int = 1

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Production Key",
                "live": True,
                "project_id": 1,
                "plan_id": 2,
            }
        }
    )


class CreateAPIKeyResponse(BaseModel):
    id: int
    name: str
    api_key: str


class APIKeyInfo(BaseModel):
    id: int
    name: str
    active: bool
    plan: str

    class Config:
        from_attributes = True


class APIKeyListResponse(BaseModel):
    api_keys: list[APIKeyInfo]


class RotateAPIKeyResponse(BaseModel):
    success: bool
    api_key: str


class MessageResponse(BaseModel):
    success: bool
    message: str