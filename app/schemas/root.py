from pydantic import BaseModel, ConfigDict


class RootResponse(BaseModel):
    name: str
    status: str
    version: str
    documentation: str
    status_page: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Nativee API",
                "status": "running",
                "version": "1.0.0",
                "documentation": "https://developer.nativee.in",
                "status_page": "https://status.nativee.in",
            }
        }
    )