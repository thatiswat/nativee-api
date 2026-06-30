from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "API Key not found"
            }
        }
    )